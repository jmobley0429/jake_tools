# edit_mode
import bpy
from bpy.types import Operator
from custom_operator import CustomOperator


class MESH_OT_quick_tris_to_quads(CustomOperator, Operator):
    bl_idname = "mesh.quick_tris_to_quads"
    bl_label = "Quick Tris to Quads"

    @classmethod
    def poll(cls, context):
        return cls.edit_obj_poll(context)

    def execute(self, context):
        bpy.ops.mesh.quads_convert_to_tris(quad_method="BEAUTY", ngon_method="BEAUTY")
        bpy.ops.mesh.tris_convert_to_quads()
        return {"FINISHED"}
