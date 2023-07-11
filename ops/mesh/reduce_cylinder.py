# edit_mode
import bpy
from bpy.types import Operator
from custom_operator import *


class MESH_OT_reduce_cylinder(CustomOperator, Operator):
    """Cut cylinder edges in half, select one edge ring and then execute."""

    bl_idname = "mesh.reduce_cylinder"
    bl_label = "Reduce Cylinder Edges"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return cls.edit_obj_poll(context)

    def execute(self, context):
        bpy.ops.mesh.edgering_select("INVOKE_DEFAULT")
        bpy.ops.mesh.select_nth()
        bpy.ops.mesh.loop_multi_select(ring=False)
        bpy.ops.mesh.dissolve_mode(use_verts=True)
        return {"FINISHED"}
