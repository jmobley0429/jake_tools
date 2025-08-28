import bpy
from bpy import data as D
from bpy import context as C

import bmesh
import utils
import numpy as np
from mathutils import Vector


class OriginSetter:

    def __init__(self, context):
        self.obj = C.edit_object
        self.mesh = self.obj.data
        self.mw = self.obj.matrix_world
        self.bm = bmesh.from_edit_mesh(self.mesh)
        self.bm.select_flush(True)
        self.bm.verts.ensure_lookup_table()

    @property
    def sel_verts(self):
        sel_verts = np.array([self.mw @ v.co for v in self.bm.verts if v.select])
        return sel_verts

    def get_center_of_sel(self):
        sel_verts = self.sel_verts
        x_locs = sel_verts[:, 0]
        y_locs = sel_verts[:, 1]
        z_locs = sel_verts[:, 2]
        center_vec = x_locs.mean(), y_locs.mean(), z_locs.mean()
        center_vec = Vector(center_vec)
        return center_vec

    def set_origin_to_sel(self):
        obj_loc = self.mw.translation.copy()
        center_vec = self.get_center_of_sel()
        dist_vec = center_vec - obj_loc

        # print(f"CENTER_VEC: {center_vec}")
        # print(f"OBJ_LOC: {obj_loc}")
        # print(f"DIST_VEC: {dist_vec}")

        bmesh.ops.translate(self.bm, verts=self.bm.verts[:], vec=-dist_vec)
        bmesh.update_edit_mesh(self.mesh)
        self.bm.free()
        self.obj.location += dist_vec


class MESH_OT_set_origin_to_edit_mode_selection(bpy.types.Operator):
    """Set object origin to Edit Mode selection"""

    bl_idname = "mesh.set_origin_to_edit_mode_selection"
    bl_label = "Origin to Selection"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == "MESH" and "EDIT" in context.mode

    def execute(self, context):
        setter = OriginSetter(context)
        setter.set_origin_to_sel()
        return {"FINISHED"}
