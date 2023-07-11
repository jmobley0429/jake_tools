import bpy
from bpy.types import Operator

class IMAGE_OT_toggle_uv_sync_selection(Operator):
    bl_idname = "uv.toggle_uv_sync_selection"
    bl_label = "Toggle Sync"
    bl_description = "Toggle Sync"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object is not None
        area_type = context.area.type == "IMAGE_EDITOR"
        mode = "EDIT" in context.mode
        return all([obj, area_type, mode])

    def execute(self, context):
        tools = context.scene.tool_settings
        bpy.context.scene.tool_settings.use_uv_select_sync = not tools.use_uv_select_sync
        return {"FINISHED"}