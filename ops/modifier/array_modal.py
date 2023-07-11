import bpy
import numpy as np
from bpy.types import Operator
from custom_operator import *

class ArrayModalOperator(CustomModalOperator, Operator):
    bl_idname = "object.array_modal"
    bl_label = "Array Modal"
    constant: bpy.props.BoolProperty(default=True)
    relative: bpy.props.BoolProperty(default=False)
    offset: bpy.props.FloatProperty(default=0.0)
    count: bpy.props.IntProperty()
    working_axes = {"X": True, "Y": False, "Z": False}

    @property
    def current_axes(self):
        return [ax for ax, val in self.working_axes.items() if val]

    @property
    def array(self):
        obj = self.get_active_obj()
        return obj.modifiers[self.mod_name]

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type in {"MESH", "CURVE"}

    def _set_axis_values(self, axes: list, value, single=True):
        array_axes = ['X', 'Y', 'Z']
        if single:
            self._set_axis_values(array_axes, 0, single=False)
        for a in axes:
            index = array_axes.index(a)
            if self.constant:
                self.modifier.constant_offset_displace[index] = value
            else:
                self.modifier.relative_offset_displace[index] = value

    def _set_array_count(self, event_type):
        value = 1
        if event_type == 'WHEELDOWNMOUSE':
            value = -1
        self.modifier.count += value

    def _report_modal_status(self, context):
        type = "CONSTANT"
        if self.relative:
            type = "RELATIVE"
        msg = [
            f'COUNT: {self.modifier.count}',
            f'OFFSET: {self.offset:.2f}',
            f'AXIS: {",".join(self.current_axes)}',
            f'TYPE: {type}',
        ]
        context.area.header_text_set(' '.join(msg))

    def modal(self, context, event):
        self._report_modal_status(context)
        # handle axis changing
        if event.type in {'X', "Y", "Z"}:
            if event.value == 'PRESS':
                ax = event.type
                # if pressing shift, XYZ will add or remove
                # itself from active axes
                if event.shift:
                    cur_val = self.working_axes[ax]
                    self.working_axes[ax] = not cur_val
                # otherwise toggle axes individually
                else:
                    for axis, value in self.working_axes.items():
                        self.working_axes[axis] = False
                    self.working_axes[ax] = True
        if event.type == "MIDDLEMOUSE":
            return {'PASS_THROUGH'}

        if event.type in {'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            self._set_array_count(event.type)

        if event.type == "TAB":
            if event.value == "PRESS":
                self.constant = not self.constant
                self.relative = not self.relative

        if event.type == 'MOUSEMOVE':
            multiplier = 0.1
            if event.shift:
                multiplier = 0.01
            delta = self.initial_mouse - event.mouse_x
            if event.ctrl:
                snap_val = np.floor(delta * (-multiplier)) + 1
                self.offset = snap_val
            else:
                self.offset = delta * (-multiplier)
            self.modifier.use_constant_offset = self.constant
            self.modifier.use_relative_offset = self.relative
            self._set_axis_values(self.current_axes, self.offset)

        elif event.type == 'LEFTMOUSE':
            self._clear_info(context)
            self.close_modifiers()
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            self._clear_info(context)
            bpy.ops.object.modifier_remove(modifier=self.modifier.name)
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        obj = self.get_active_obj()
        array = obj.modifiers.new(name='Array', type="ARRAY")
        array.use_constant_offset = True
        array.use_merge_vertices = True
        array.use_merge_vertices_cap = True
        array.use_relative_offset = False
        self.mod_name = array.name
        self._set_axis_values(self.current_axes, self.offset)

        if context.object:
            self.initial_mouse = event.mouse_x
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}