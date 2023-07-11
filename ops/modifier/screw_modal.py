#modifier
import utils
import bpy
import numpy as np
from bpy.types import Operator
from custom_operator import *

class ScrewModalOperator(CustomModalOperator, Operator):
    bl_idname = "object.screw_modal"
    bl_label = "Screw Modal"

    mod_name: bpy.props.StringProperty()
    screw_offset: bpy.props.FloatProperty()
    angle: bpy.props.FloatProperty()
    steps: bpy.props.IntProperty()
    initial_mouse: bpy.props.FloatProperty()
    iterations: bpy.props.IntProperty()
    axis: bpy.props.StringProperty()
    use_object_screw_offset: bpy.props.BoolProperty()
    use_normal_calculate: bpy.props.BoolProperty()
    use_normal_flip: bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type in {"MESH", "CURVE"}

    def set_screw_angle(self, delta, multiplier):
        angle = delta * multiplier
        new_angle = self.modifier.angle - np.radians(angle)
        self.modifier.angle = utils.clamp(new_angle, 0, 2 * np.pi)

    def set_screw_count(self, event_type):
        if event_type == "WHEELUPMOUSE":
            self.modifier.steps += 1
        else:
            self.modifier.steps -= 1

    def _log_info_msg(self):
        mod = self.modifier
        msg = [
            f"Degrees: {np.degrees(mod.angle)}",
            f"Steps: {mod.steps}",
            f"Offset: {mod.screw_offset}",
            f"Iterations: {mod.iterations}",
            f"Screw Axis: {mod.axis}",
        ]
        return ', '.join(msg)

    def modal(self, context, event):
        self.display_modal_info(self._log_info_msg(), context)
        if event.type == 'MOUSEMOVE':
            multiplier = 0.1
            if event.shift:
                multiplier = 0.01
            delta = self.initial_mouse - event.mouse_x
            self.set_screw_angle(delta, multiplier)

        if event.type in self.wheel_input:
            self.set_screw_count(event.type)

        if event.type in self.numpad_input:
            if event.value == "PRESS":
                if event.type == "NUMPAD_ENTER":
                    self.modifier.steps = self.int_numpad_value
                    self.numpad_value = []
                if event.type == "BACK_SPACE":
                    self.numpad_value.pop()
                else:
                    value = event.unicode
                    self.numpad_value.append(value)

        elif event.type == 'LEFTMOUSE':
            return self.exit_modal(context)

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return self.exit_modal(context, cancelled=True)

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.object:
            obj = self.get_active_obj()
            bpy.ops.object.modifier_add(type="SCREW")
            mod = self._get_last_modifier()
            self.initial_mouse = event.mouse_x
            self.mod_name = mod.name
            self.modifier.steps = mod.steps
            self.modifier.screw_offset = 0
            self.modifier.angle = np.radians(360)
            self.modifier.iterations = 1
            self.modifier.axis = "Z"
            self.modifier.use_object_screw_offset = False
            self.modifier.use_normal_calculate = True
            self.modifier.use_normal_flip = False
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            return {'CANCELLED'}