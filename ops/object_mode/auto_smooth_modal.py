import bpy
from bpy.types import Operator
from custom_operator import *
import numpy as np


class SSObject:
    def __init__(self, obj):
        self.obj = obj
        self.mesh = obj.data

    @property
    def is_auto_smoothed(self):
        return True
        # return self.mesh.use_auto_smooth

    def _set_active(self, context):
        context.view_layer.objects.active = self.obj

    def set_ss_angle(self, angle):
        self.mesh.auto_smooth_angle = angle

    def add_custom_normals(self, context, clear=False):
        self._set_active(context)
        if clear:
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
        else:
            bpy.ops.mesh.customdata_custom_splitnormals_add()

    def set_smooth_shaded(self, angle):
        print(f"Setting active obj: {self.obj.name}")
        bpy.ops.mesh.customdata_custom_splitnormals_clear()
        # self.mesh.use_auto_smooth = True
        self.mesh.auto_smooth_angle = angle


class SmoothShader(OperatorBaseClass):
    def __init__(self, context, args, op):
        super().__init__(context, args, op)
        self.selected_objects = context.selected_objects[:]
        self.ss_objs = [SSObject(obj) for obj in self.selected_objects]
        self.is_smooth_shaded = True
        self.current_angle = 40
        # self.toggle_custom_normals()
        self.has_custom_normals = True

    @property
    def modal_info_string(self):
        if self.is_smooth_shaded:
            ss_msg = "Smooth"
        else:
            ss_msg = "Flat"
        msg = [
            f"AUTO SMOOTH ANGLE (Wheel): {int(self.current_angle)}",
            f"USE CUSTOM SPLIT NORMALS (N): {self.has_custom_normals}",
            f"SHADE MODE (S): {ss_msg}",
        ]

        return ", ".join(msg)

    def toggle_custom_normals(self, clear=False):
        for obj in self.ss_objs:
            obj.add_custom_normals(self.context, clear=clear)

    def set_objs_to_smooth_shaded(self):
        for obj in self.ss_objs:
            obj._set_active(self.context)
            obj.set_smooth_shaded(self.current_angle)
        # print("is auto_smoothed: ", obj.mesh.use_auto_smooth)
        # print("AS angle: ", obj.mesh.auto_smooth_angle)

    def set_objs_to_flat_shaded(self):
        for obj in self.ss_objs:
            obj.set_flat_shaded(self.context)

    def toggle_shading(self, obj):
        if not self.is_smooth_shaded:
            self.set_objs_to_smooth_shaded()

        else:
            self.set_objs_to_flat_shaded()

    def set_new_angle_val(self, raw_angle, divisor=5):
        if divisor == 5:
            raw_angle = round(raw_angle / divisor) * divisor
        self.current_angle = raw_angle
        print(self.current_angle)
        print(self._current_angle_rads)
        for obj in self.ss_objs:
            obj.set_ss_angle(self._current_angle_rads)

    @property
    def _current_angle_rads(self):
        return np.radians(self.current_angle)

    def change_smoothing_angle(self, event, set_angle=False):
        if set_angle:
            self.set_new_angle_val(self.current_angle, divisor=1)
            return
        addend = 5
        if event.shift:
            addend = 1
        divisor = addend
        if event.type == "WHEELDOWNMOUSE":
            addend *= -1
        raw_angle = self.current_angle + addend
        self.set_new_angle_val(raw_angle, divisor=divisor)


class OBJECT_OT_set_auto_smooth_modal(CustomModalOperator, Operator):
    bl_idname = "object.auto_smooth_modal"
    bl_label = "Set Auto Smooth"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def invoke(self, context, event):
        self.in_edit = self.in_mode(context, "EDIT")
        self.overlays_on = context.space_data.overlay.show_overlays
        if self.in_edit:
            self.to_mode("OBJECT")
        # bpy.ops.object.shade_smooth(use_auto_smooth=True)
        if self.overlays_on:
            context.space_data.overlay.show_overlays = False

        self.shader = SmoothShader(
            context,
            self.as_keywords(),
            self,
        )
        # self.shader.set_objs_to_smooth_shaded()
        context.window_manager.modal_handler_add(self)
        print("running")
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        shader = self.shader
        if event.value == "PRESS":
            if event.type == "N":
                self.shader.toggle_custom_normals(self.shader.has_custom_normals)
            elif event.type == "TAB":
                self.shader.toggle_shading()
            # elif event.type == "S":
            #     shader.toggle_auto_smooth_(context)
            elif event.type == "LEFTMOUSE":
                context.space_data.overlay.show_overlays = self.overlays_on
                if self.in_edit:
                    self.to_mode("EDIT")
                return self.exit_modal(context)

            elif event.type in {"RIGHTMOUSE", "ESC"}:
                context.space_data.overlay.show_overlays = self.overlays_on
                if self.in_edit:
                    self.to_mode("EDIT")
                return self.exit_modal(context, cancelled=True)
            elif event.type in {"WHEELUPMOUSE", "WHEELDOWNMOUSE"}:
                shader.change_smoothing_angle(event)
            elif event.type in self.numpad_input:
                if event.type == "NUMPAD_ENTER":
                    self.current_angle = self.float_numpad_value
                    self.change_smoothing_angle(context, event, set_angle=True)
                    self.numpad_value = []
                else:
                    self.set_numpad_input(event)

        self.display_modal_info(shader.modal_info_string, context)
        return {"RUNNING_MODAL"}


kms = [
    {
        "keymap_operator": OBJECT_OT_set_auto_smooth_modal.bl_idname,
        "name": "Object Mode",
        "letter": "H",
        "shift": 0,
        "ctrl": 1,
        "alt": 1,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {},
    }
]
