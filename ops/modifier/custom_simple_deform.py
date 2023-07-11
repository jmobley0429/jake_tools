#modifier

import bpy
import numpy as np
from bpy.types import Operator
from custom_operator import *
import utils

class CustomSimpleDeform(CustomModalOperator, Operator):
    """Add Custom Simple Deform Modifier"""

    bl_idname = "object.custom_simple_deform"
    bl_label = "Add Custom Simple Deform"
    bl_options = {"REGISTER", "UNDO"}

    angle: bpy.props.FloatProperty(name='angle', description='Deform Angle', default=45.0)
    axis: bpy.props.StringProperty(name='axis', description='Deform Axis', default="Z")
    x: bpy.props.IntProperty(min=0, max=360)
    mod = None

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type in {"MESH", "CURVE"}

    def invoke(self, context, event):
        obj = self.get_active_obj()
        bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
        self.mod = self._get_last_modifier()
        self.mod.deform_method = 'BEND'
        self.mod.deform_axis = 'Z'
        self.init_x = event.mouse_x
        self.x = 0
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        msg = f'Angle: {self.angle}, Axis: {self.axis}'
        self.display_modal_info(msg, context)
        if event.type == 'MOUSEMOVE':
            delta = int((event.mouse_x) - self.init_x)
            self.angle = utils.clamp(delta, 0, 360)
            self.mod.angle = np.radians(self.angle)
        elif event.type in {"X", "Y", "Z"}:
            self.axis = event.type
            self.mod.deform_axis = self.axis

        elif event.type == 'LEFTMOUSE':  # Confirm
            self._clear_info(context)
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
            self._clear_info(context)
            bpy.ops.object.modifier_remove(modifier=self.mod.name)
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}