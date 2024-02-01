import bpy
from bpy.props import IntProperty, FloatProperty


class MODIFIER_OT_add_weld_modal(bpy.types.Operator):
    """Move an object with the mouse, example"""

    bl_idname = "modifier.weld_modifier_modal"
    bl_label = "Add Weld Modal"

    first_mouse_x: IntProperty()
    first_value: FloatProperty()

    def modal(self, context, event):
        mult = 0.01
        if event.shift:
            mult = 0.001

        if event.type == "MOUSEMOVE":
            delta = self.first_mouse_x - event.mouse_x
            self.modifier.merge_threshold = self.first_value + delta * mult

        elif event.type == "LEFTMOUSE":
            return {"FINISHED"}

        elif event.type in {"RIGHTMOUSE", "ESC"}:
            context.object.modifiers.remove(self.modifier)
            return {"CANCELLED"}

        return {"RUNNING_MODAL"}

    def invoke(self, context, event):
        if context.object:
            self.first_mouse_x = event.mouse_x
            self.modifier = context.object.modifiers.new(type="WELD", name="Weld")
            self.merge_threshold = 0.001
            self.modifier.merge_threshold = self.merge_threshold

            context.window_manager.modal_handler_add(self)
            return {"RUNNING_MODAL"}
        else:
            self.report({"WARNING"}, "No active object, could not finish")
            return {"CANCELLED"}
