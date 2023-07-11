#modifier

import bpy
import numpy as np
from bpy.types import Operator
from custom_operator import *

class CustomShrinkwrap(CustomOperator, Operator):
    """Add Custom Shrinkwrap Modifier"""

    bl_options = {"REGISTER", "UNDO"}

    bl_idname = "object.custom_shrinkwrap"
    bl_label = "Add Custom Shrinkwrap"

    apply_projection = False

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type in {"MESH", "CURVE"}

    def invoke(self, context, event):
        if event.alt:
            self.apply_projection = True
        return self.execute(context)

    def execute(self, context):
        num_objs = len(bpy.context.selected_objects)
        if num_objs < 2:
            bpy.ops.object.modifier_add(type="SHRINKWRAP")
            self.apply_projection = False
        else:
            mod, target = self.get_mod_and_target_objects()
            bpy.context.view_layer.objects.active = mod
            bpy.ops.object.modifier_add(type="SHRINKWRAP")
        sw = self._get_last_modifier()
        sw.target = target
        sw.wrap_mode = "ABOVE_SURFACE"
        sw.show_on_cage = True
        sw.offset = 0.0001
        if self.apply_projection:
            for mod in mod.modifiers[:]:
                if mod.type in {"SUBSURF", "SHRINKWRAP"}:
                    bpy.ops.object.modifier_apply(modifier=mod.name)
        return {"FINISHED"}