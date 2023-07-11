# edit_mode

import bmesh
import bmesh_utils
from custom_operator import *
import bpy


class CopyBevelWeights(EditModeOperatorBaseClass):
    def __init__(self, context):
        super().__init__(context)
        self.mesh = context.edit_object.data
        self.bm = bmesh_utils.get_bmesh(context)
        self.bw_layer = self.bm.edges.layers.bevel_weight.verify()
        self.bm.edges.ensure_lookup_table()
        self.get_edge_weight_value()

    def get_edge_weight_value(self):
        edge = self.bm.select_history.active
        self.weight = edge[self.bw_layer]

    def set_edge_weight(self, edge):
        edge[self.bw_layer] = self.weight

    def execute(self):
        for edge in self.sel_edges[:]:
            self.set_edge_weight(edge)
        bmesh.update_edit_mesh(self.mesh)
        self.cleanup_bmesh()


class MESH_OT_copy_edge_bevel_weights(CustomOperator, bpy.types.Operator):
    bl_idname = "mesh.copy_edge_bevel_weight_from_active"
    bl_label = "Copy Edge Bevel Weight From Active"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return cls.edit_obj_poll(context)

    def execute(self, context):
        cbw = CopyBevelWeights(context)
        cbw.execute()
        return {"FINISHED"}
