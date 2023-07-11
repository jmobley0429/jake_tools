#modifier

import bpy
import numpy as np
from bpy.types import Operator
from custom_operator import *

class RadialArray(OperatorBaseClass):

    def __init__(self, context, args, op):
        super().__init__(context, args, op)
        self.active_object_offset = self._active_obj.location.y
        self.current_mode = "ROTATE"
        self.add_empty_obj()

    
    def add_empty_obj(self):
        self.empty = bpy.data.objects.new(name=f"{self._active_obj.name}_RadialArrayOffset", object_data=None) 
        self.context.collection.objects.link(self.empty)
        self.empty.location = self._active_obj.location

    
    def add_array_mod(self):
        mod = self._active_obj.modifiers.new(name="RadialArray", type="ARRAY")
        mod.use_object_offset = True 
        mod.use_relative_offset = False
        mod.offset_object = self.empty
        self._array_mod = mod

    @property
    def _rotation_value(self):
        count = self.array_count 
        print("DEG: ", self.degrees, "COUNT: ", count)
        rotation_degrees = self.degrees / count
        return np.radians(rotation_degrees)

    def set_empty_rotation(self):
        self.empty.rotation_euler.z = self._rotation_value

    def _report_modal_status(self):
        type = "CONSTANT"
        msg = [
            f'COUNT: {self.array_count}'
            f'DEGREES: {self.degrees}'
        ]
        self.context.area.header_text_set(' '.join(msg))

    def _set_array_count(self, event_type):
        value = 1
        if event_type == 'WHEELDOWNMOUSE':
            value = -1
        self.array_count += value
        self._array_mod.count = self.array_count

    def round_degree_amt(self, offset):
        return min(0, max(360, offset))
    
    def set_degrees(self, offset):
        self.degrees = offset

    def set_object_offset(self, offset):
        offset_val = offset * .001
        self._active_obj.location.y = offset_val

    def set_modal_offset(self, offset):
        if self.current_mode == "MOVE":
            self.set_object_offset(offset)
            self.set_object_offset(offset)
        else:
            self.set_degrees(offset)
            self.set_empty_rotation()

    def set_current_mode(self, event):
        modes = ['MOVE', 'ROTATE']
        events = ['G', 'R']
        eid = events.index(event.type)
        self.current_mode = modes[eid]


def radial_array_debug_setup(context):
    ao = context.view_layer.objects.active
    for mod in ao.modifiers[:]:
        ao.modifiers.remove(mod)
    for obj in bpy.data.objects[:]:
        if obj.type == "EMPTY":
            bpy.data.objects.remove(obj, do_unlink=True)

class OBJECT_OT_RadialArrayModal(CustomModalOperator, Operator):
    bl_idname = "object.radial_array_modal"
    bl_label = 'Radial Array Modal'
    bl_options = {"REGISTER", "UNDO"}

    array_count: bpy.props.IntProperty(name="Array Count", description='Number of objects in the array', default=1)
    degrees: bpy.props.FloatProperty(name="Array Count", description='Number of objects in the array', default=360)

    @classmethod
    def poll(cls, context):
        conditions = [
            context.active_object is not None,
            context.active_object.type in {"MESH", "CURVE"},
            context.mode == "OBJECT"

        ]
        return all(conditions)
    
    def invoke(self, context, event):
        radial_array_debug_setup(context)
        self.RadialArray = RadialArray(context, self.as_keywords(), self)
        self.RadialArray.add_array_mod()
        self.initial_mouse = event.mouse_x
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    
    def modal(self, context, event):
        ra = self.RadialArray
        ra._report_modal_status()
        if event.type in {"G", "R"}:
            if event.value == 'PRESS':
                ra.set_current_mode(event) 


        if event.type in {'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            ra._set_array_count(event.type)

        if event.type == 'MOUSEMOVE':
            multiplier = 1.0
            if event.shift:
                multiplier = 0.1
            delta = self.initial_mouse - event.mouse_x
            if event.ctrl:
                snap_val = (np.floor(delta * (-multiplier)) )
                offset = snap_val
            else:
                offset = delta * (-multiplier)
            ra.set_modal_offset(offset)
            
            

        elif event.type == 'LEFTMOUSE':
            self._clear_info(context)
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            self._clear_info(context)
            ra._active_obj.modifiers.remove(ra._array_mod)
            return {'CANCELLED'}        
        return {"RUNNING_MODAL"}