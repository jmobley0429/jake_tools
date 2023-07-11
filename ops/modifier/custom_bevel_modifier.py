#modifier

import bpy
import numpy as np
from bpy.types import Operator
from custom_operator import *


class BevelModifier(CustomOperator):

    bl_options = {'REGISTER', "UNDO"}

    limit_method: bpy.props.EnumProperty(
        items=(
            ('WEIGHT', "Weight", "Weight"),
            ('ANGLE', "Angle", "Weight"),
        ),
        name='Weight',
        description='Weighted Limit Method',
        default="ANGLE",
    )

    def _next_limit_method(self, event):
        methods = [
            'WEIGHT',
            'ANGLE',
        ]
        addend = 1
        if event.shift:
            addend = -1
        curr_index = methods.index(self.limit_method)
        new_index = (curr_index + addend) % len(methods)
        return methods[new_index]

    @property
    def relative_bwidth(self):
        obj = self.get_active_obj()
        return np.mean(obj.dimensions) / 65

    def _add_bevel_modifier(self, harden_normals=True, profile=0.5, angle_limit=45):
        in_edit_mode = bool(bpy.context.object.mode == "EDIT")
        if in_edit_mode:
            bpy.ops.object.mode_set(mode="OBJECT")
        obj = self.get_active_obj()
        bpy.ops.object.shade_smooth()
        obj.data.use_auto_smooth = True
        bpy.ops.object.modifier_add(type='BEVEL')
        bevel_mod = obj.modifiers[:][-1]
        bevel_mod.limit_method = self.limit_method
        bevel_mod.segments = 2
        bevel_mod.width = self.relative_bwidth
        bevel_mod.profile = profile
        bevel_mod.angle_limit = np.radians(angle_limit)
        bevel_mod.harden_normals = harden_normals
        bevel_mod.miter_outer = "MITER_ARC"
        bevel_mod.use_clamp_overlap = False
        self.bevel_mod = bevel_mod
        if in_edit_mode:
            bpy.ops.object.mode_set(mode="EDIT")


class CustomAddBevelModifier(BevelModifier, CustomModalOperator, Operator):
    """Add Custom Bevel Modifier"""

    bl_idname = "object.custom_bevel_modifier"
    bl_label = "Add Custom Bevel"
    bl_parent_id = "CustomOperator"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Add Bevel modifier, Angle is default limit method, Hold ALT for Weighted."

    @property
    def modal_info_string(self):
        lines = [
            f"BEVEL WIDTH: {self.bevel_mod.width:.3f}",
            f"SEGMENTS (MouseWheel): {self.bevel_mod.segments}",
            f"LIMIT METHOD (Tab): {self.limit_method}",
            f"CLAMP OVERLAP (C): {self.bevel_mod.use_clamp_overlap}",
            f"HARDEN NORMALS (H): {self.bevel_mod.harden_normals}",
        ]
        return ", ".join(lines)

    def invoke(self, context, event):
        if event.alt:
            self.limit_method = "WEIGHT"
        self._add_bevel_modifier()
        self.init_mouse_x = event.mouse_x
        self.bwidth = self.relative_bwidth
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def modal(self, context, event):

        self.display_modal_info(self.modal_info_string, context)
        self.multiplier = 0.001
        if event.shift:
            self.multiplier = 0.0001
        if event.type == "MOUSEMOVE":

            delta = (self.init_mouse_x - event.mouse_x) * self.multiplier
            self.bevel_mod.width -= delta
            self.init_mouse_x = event.mouse_x
        elif event.type == "WHEELUPMOUSE":
            self.bevel_mod.segments += 1
        elif event.type == "WHEELDOWNMOUSE":
            self.bevel_mod.segments -= 1
        elif event.value == "PRESS":
            if event.type == "TAB":
                new_lm = self._next_limit_method(event)
                self.bevel_mod.limit_method = new_lm
            elif event.type == "C":
                col = self.bevel_mod.use_clamp_overlap
                self.bevel_mod.use_clamp_overlap = not col
            elif event.type == "H":
                hn = self.bevel_mod.harden_normals
                self.bevel_mod.harden_normals = not hn
        elif event.type in {"ESC", "RIGHTMOUSE"}:
            bpy.ops.object.modifier_remove(modifier=self.bevel_mod.name)
            return self.exit_modal(context, cancelled=True)
        elif event.type == "LEFTMOUSE":
            return self.exit_modal(context)
        return {"RUNNING_MODAL"}
    
class CustomAddQuickBevSubSurfModifier(BevelModifier, Operator):
    """Add Custom Bevel Modifier with Subsurf"""

    bl_idname = "object.custom_bevel_subsurf_modifier"
    bl_label = "Add Custom Bevel Subsurf"
    bl_parent_id = "CustomAddBevelModifier"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = self.get_active_obj()
        in_edit = "EDIT" in context.mode
        if in_edit:
            bpy.ops.object.mode_set(mode="OBJECT")
        self._add_bevel_modifier(profile=1.0)
        
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.ops.object.modifier_add(type='WEIGHTED_NORMAL')
        bpy.ops.object.shade_smooth()
        obj.data.use_auto_smooth = True
        self.close_modifiers()
        if in_edit:
            bpy.ops.object.mode_set(mode="EDIT")
        return {"FINISHED"}