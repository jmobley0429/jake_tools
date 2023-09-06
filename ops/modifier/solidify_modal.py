#modifier

import bpy
import numpy as np
from bpy.types import Operator
from custom_operator import *



class SolidifyModalOperator(CustomModalOperator, Operator):
    bl_idname = "object.solidify_modal"
    bl_label = "Solidify Modal"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type in {"MESH", "CURVE"}

    thickness: bpy.props.FloatProperty()

    def increment_offset_index(self):
        self.offset_index = (self.offset_index + 1) % 3

    def modal(self, context, event):
        msg = f"Thickness: {self.thickness}, Offset (F): {self.offsets[self.offset_index]}"
        
        if self.numpad_value:
            msg += f" Value: {self.string_numpad_value}"
        context.area.header_text_set(msg)
        if event.type == 'MOUSEMOVE':
            multiplier = 0.01
            if event.shift:
                multiplier = 0.001
            self.thickness = self._initial_mouse - event.mouse_x
            self.solidify_mod.thickness = (self.thickness * multiplier) * -1

        if event.type == 'F':
            if event.value == "PRESS":
                self.increment_offset_index()
                self.solidify_mod.offset = self.offsets[self.offset_index]

        if event.type in self.numpad_input:
            if event.value == "PRESS":
                if event.type == "NUMPAD_ENTER":
                    self.solidify_mod.thickness = self.float_numpad_value
                    return self.exit_modal(context)
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
            self.offsets = [1.0, 0.0, -1.0]
            self.offset_index = 0
            obj = self.get_active_obj()
            mod = obj.modifiers.new(name="Solidify", type="SOLIDIFY")
            
            mod.use_even_offset = True
            mod.offset = self.offsets[self.offset_index]
            mod.use_quality_normals = True
            mod.solidify_mode = "NON_MANIFOLD"
            self.mod_name = mod.name
            self.thickness = mod.thickness
            self.solidify_mod = mod
            self._initial_mouse = event.mouse_x
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            return {'CANCELLED'}