#modifier

from bpy.types import Operator
from custom_operator import *

class CustomWeightedNormal(CustomOperator, Operator):
    """Add Custom Weighted Normal Modifier"""

    bl_idname = "object.custom_weighted_normal"
    bl_label = "Add Custom Weighted Normal"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type in {"MESH"}

    def execute(self, context):
        obj = self.get_active_obj()
        obj.data.use_auto_smooth = True
        mod = obj.modifiers.new('Weighted Normal', type="WEIGHTED_NORMAL")
        mod.keep_sharp = True
        self.close_modifiers()

        return {"FINISHED"}