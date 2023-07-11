import bpy
from bpy.types import Operator


class IMAGE_OT_pack_with_mode(Operator):
    bl_idname = "uv.pack_with_mode"
    bl_label = "Pack"
    bl_description = "UVPackmaster Pack (ALT to use Blender Default Pack)"
    bl_options = {"REGISTER", "UNDO"}

    mode = None

    def invoke(self, context, event):
        if event.alt:
            self.mode = "DEFAULT"
        return self.execute(context)

    def execute(self, context):
        if self.mode is None:
            bpy.ops.uvpackmaster2.uv_pack()
        else:
            bpy.ops.uv.pack_islands()
        return {"FINISHED"}
