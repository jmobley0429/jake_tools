# modifier

import bpy
import numpy as np
from bpy.types import Operator
from custom_operator import *


class CustomRemesh(CustomOperator, Operator):
    """Add Custom Remesh Modifier"""

    bl_idname = "object.custom_remesh"
    bl_label = "Add Custom Remesh"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type in {"MESH", "CURVE"}

    def execute(self, context):
        bpy.ops.object.modifier_add(type="REMESH")
        mod = self._get_last_modifier()
        mod.voxel_size = 0.025
        mod.use_smooth_shade = True
        return {"FINISHED"}
