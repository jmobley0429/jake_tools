# modifier

import bpy
import numpy as np
from bpy.types import Operator
from custom_operator import *


class CustomDecimate(CustomOperator, Operator):
    """Add Custom Decimate Modifier"""

    bl_options = {"REGISTER", "UNDO"}

    bl_idname = "object.custom_decimate"
    bl_label = "Add Custom Decimate"
    bl_description = "ALT > Add modifier and apply immediately, CTRL > Add planar modifier."

    apply_mod = False
    dec_type = "COLLAPSE"
    mode = None

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type in {"MESH", "CURVE"}

    def invoke(self, context, event):
        self.mode = self.get_current_mode(context)
        if event.alt:
            self.apply_mod = True
        if event.ctrl:
            self.dec_type = "DISSOLVE"
        return self.execute(context)

    def execute(self, context):
        switch_mode = self.mode in {"EDIT", "SCULPT"}
        if switch_mode:
            self.to_mode("OBJECT")
        for obj in context.selected_objects[:]:
            if obj.type in {"MESH",}:
                mod = obj.modifiers.new(name="Decimate", type="DECIMATE")
                mod.decimate_type = self.dec_type
                if self.dec_type == "COLLAPSE":
                    mod.ratio = 0.2
                if self.apply_mod:
                    bpy.ops.object.modifier_apply(modifier=mod.name)
            if switch_mode:
                self.to_mode(self.mode)
        return {"FINISHED"}
