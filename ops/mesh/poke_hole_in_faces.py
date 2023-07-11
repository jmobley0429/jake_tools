# edit_mode

import bmesh
import numpy as np
from custom_operator import *
import bpy


class MESH_OT_poke_hole_in_faces(
    CustomBmeshOperator, CustomModalOperator, bpy.types.Operator
):
    bl_idname = "mesh.poke_hole_in_faces"
    bl_label = "Poke Hole in Face"
    bl_options = {"REGISTER", "UNDO"}

    offset_multiplier: bpy.props.FloatProperty(name="Offset Multiplier", default=0.2)
    bridge = False

    @classmethod
    def poll(cls, context):
        return cls.edit_obj_poll(context)

    def poke_hole(self):
        ret = bmesh.ops.poke(self.bm, faces=self.sel_faces)
        center = ret["verts"][:]
        self.select_elem_in_list(self.bm.verts[:], center)
        del ret
        for face in self.bm.faces[:]:
            face.select_set(False)
        self.bm.select_flush_mode()
        ret = bmesh.ops.bevel(self.bm, geom=center, offset=self.offset_amt, segments=2)
        verts = ret["verts"]
        faces = ret["faces"]
        del ret
        bmesh.ops.delete(self.bm, geom=faces, context="FACES")
        self.select_elem_in_list(self.bm.verts[:], verts)
        bmesh.update_edit_mesh(self.mesh)
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type="VERT")
        bpy.ops.mesh.looptools_circle()

    def invoke(self, context, event):
        self.bmesh(context)
        self.sel_faces = [f for f in self.bm.faces[:] if f.select]
        self.offset_amt = (
            np.mean([f.calc_area() for f in self.sel_faces]) * self.offset_multiplier
        )
        # self.init_mouse_x = event.mouse_x
        if event.alt:
            self.bridge = True
        return self.execute(context)

    def execute(self, context):
        self.poke_hole()
        if self.bridge:
            bpy.ops.mesh.bridge_edge_loops()
        return {"FINISHED"}
