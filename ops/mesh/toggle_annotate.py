# edit_mode
import bpy
from bpy.types import Operator
from custom_operator import *


class ToggleAnnotateProps(bpy.types.PropertyGroup):
    scene_prop_id = "ToggleAnnotateProps"
    bl_idname = "ToggleAnnotateProps"
    prev_tool: bpy.props.StringProperty()


class VIEW3D_OT_toggle_annotate(Operator):
    bl_idname = "view3d.toggle_annotate"
    bl_label = "Toggle Annotate"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        self.mode = context.mode
        self.props = context.window_manager.ToggleAnnotateProps
        self.prev_tool = self.props.prev_tool
        return self.execute(context)

    def execute(self, context):
        tools = context.workspace.tools
        curr_tool = tools.from_space_view3d_mode(self.mode, create=False).idname
        if self.prev_tool is None or curr_tool != "builtin.annotate":
            bpy.ops.wm.tool_set_by_id(name="builtin.annotate")
        else:
            bpy.ops.wm.tool_set_by_id(name=self.prev_tool)
        context.window_manager.ToggleAnnotateProps.prev_tool = curr_tool
        return {"FINISHED"}


def register():
    print("REGISTERING: **********************\n" * 5)
    bpy.types.WindowManager.ToggleAnnotateProps = bpy.props.PointerProperty(
        type=ToggleAnnotateProps
    )


def unregister():
    del bpy.types.WindowManager.ToggleAnnotateProps
