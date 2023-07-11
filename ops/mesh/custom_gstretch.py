import bpy
from bpy.types import Operator

class MESH_OT_gstretch_override(Operator):
    bl_label = "GStretch"
    bl_idname = "mesh.custom_gstretch"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return bpy.types.MESH_OT_looptools_gstretch.poll(context)

    def execute(self, context):
        bpy.ops.mesh.looptools_gstretch()
        bpy.ops.remove.annotation()
        return {"FINISHED"}