# edit_mode

import bmesh
import bpy
import numpy as np
from bpy.types import Operator
from custom_operator import *


def basically_zero(vector):
    return all([v < 0.00001 for v in vector])


def vert_edges_are_collinear(vert):
    edges = vert.link_edges[:]
    edge_vectors = []
    for edge in edges:
        edge_vector = np.subtract(*[v.co for v in edge.verts[:]])
        edge_vectors.append(edge_vector)
    return basically_zero(np.cross(*edge_vectors))


def more_edges_than_faces(vert):
    return len(vert.link_edges) >= len(vert.link_faces)


def is_center_edge_vert(vert):
    if len(vert.link_edges) == 2:
        return more_edges_than_faces(vert) and vert_edges_are_collinear(vert)
    return False


class CenterEdgeVertFinder:
    def __init__(self, context):
        self.context = context
        self.obj = context.edit_object
        self.mesh = self.obj.data
        self.bm = bmesh.from_edit_mesh(self.mesh)

    @property
    def center_edge_verts(self):
        cevs = [vert for vert in self.bm.verts[:] if is_center_edge_vert(vert)]
        return cevs

    def cleanup_center_edge_verts(self):
        bmesh.ops.dissolve_verts(self.bm, verts=self.center_edge_verts)
        bmesh.update_edit_mesh(self.mesh)


class CleanupMesh(EditModeOperatorBaseClass):
    def __init__(self, context, args, op=None):
        super().__init__(context, args)
        if op is not None:
            self.op = op

        self.obj = context.edit_object
        self.mesh = self.obj.data
        self.bm = bmesh.from_edit_mesh(self.mesh)

    @property
    def _select_state_from_mode(self):
        modes = "VERT EDGE FACE".split()
        bm_modes = []
        for mode in modes:
            if mode in self.bm.select_mode:
                bm_modes.append(True)
            else:
                bm_modes.append(False)
        return tuple(bm_modes)

    def _finish_op(self):
        self.context.tool_settings.mesh_select_mode = self._select_state_from_mode
        self.bm.select_flush_mode()
        bmesh.update_edit_mesh(self.mesh)

    def select_short_edges(
        self,
    ):
        self.selected = 0
        for e in self.bm.edges[:]:
            e.select_set(False)
            length = e.calc_length()
            if length < self.edge_threshold:
                e.select_set(True)
                self.selected += 1
        self.bm.select_mode = {"EDGE"}
        self._finish_op()
        if not self.selected:
            self.op.report({"INFO"}, "No short edges found!")
        return {"FINISHED"}

    def select_small_faces(
        self,
    ):
        self.selected = 0
        for face in self.bm.faces[:]:
            face.select_set(False)
            area = face.calc_area()
            if area < self.face_threshold:
                face.select_set(True)
                self.selected += 1
        self.bm.select_mode = {"FACE"}
        self._finish_op()
        if not self.selected:
            self.op.report({"INFO"}, "No small faces found!")
        return {"FINISHED"}

    def select_ngons(self):
        self.selected = 0
        for face in self.bm.faces:
            if len(face.edges[:]) > 4:
                face.select_set(True)
                self.selected += 1
            else:
                face.select_set(False)
        self.bm.select_mode = {"FACE"}
        self._finish_op()
        if not self.selected:
            self.op.report({"INFO"}, "No ngons found!")
        return {"FINISHED"}

    def cleanup_ngons(self):
        self.select_ngons()
        if self.selected:
            bpy.ops.mesh.quick_tris_to_quads()
            bpy.ops.mesh.select_all(action="DESELECT")
        return {"FINISHED"}


class MESH_OT_cleanup_center_edge_verts(CustomOperator, bpy.types.Operator):
    bl_idname = "mesh.cleanup_center_edge_verts"
    bl_label = "Cleanup Center-Edge Verts"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return cls.edit_obj_poll(context)

    def execute(self, context):
        cleaner = CenterEdgeVertFinder(context)
        cleaner.cleanup_center_edge_verts()
        return {"FINISHED"}


class MESH_OT_cleanup_select_small_faces(CustomOperator, bpy.types.Operator):
    bl_idname = "mesh.cleanup_select_small_faces"
    bl_label = "Select Small Faces"

    face_threshold: bpy.props.FloatProperty(name="Face Threshold", default=0.0001)

    @classmethod
    def poll(cls, context):
        return cls.edit_obj_poll(context)

    def invoke(self, context, event):
        self.args = self.as_keywords()
        return self.execute(context)

    def execute(self, context):
        cleaner = CleanupMesh(context, self.args, op=self)
        return cleaner.select_small_faces()


class MESH_OT_cleanup_select_short_edges(CustomOperator, bpy.types.Operator):
    bl_idname = "mesh.cleanup_select_short_edges"
    bl_label = "Select Short Edges"

    edge_threshold: bpy.props.FloatProperty(name="Edge Threshold", default=0.001)

    @classmethod
    def poll(cls, context):
        return cls.edit_obj_poll(context)

    def invoke(self, context, event):
        self.args = self.as_keywords()
        return self.execute(context)

    def execute(self, context):
        cleaner = CleanupMesh(context, self.args, op=self)
        return cleaner.select_short_edges()


class MESH_OT_cleanup_handle_ngons(CustomOperator, bpy.types.Operator):
    bl_idname = "mesh.cleanup_handle_ngons"
    bl_label = "Cleanup Ngons"

    @classmethod
    def poll(cls, context):
        return cls.edit_obj_poll(context)

    def invoke(self, context, event):
        self.args = self.as_keywords()
        return self.execute(context)

    def execute(self, context):
        cleaner = CleanupMesh(context, self.args, op=self)
        return cleaner.cleanup_ngons()
