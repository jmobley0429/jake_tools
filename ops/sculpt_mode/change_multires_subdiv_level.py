import bpy
from bpy.types import Operator
from custom_operator import *
import utils


class SCULPT_OT_change_multires_subdiv_level(CustomOperator, Operator):
    bl_idname = "sculpt.change_multires_subdiv_level"
    bl_label = "Change Multires Subdiv Level"
    bl_options = {'REGISTER', 'UNDO'}

    inc_dec: bpy.props.EnumProperty(
        items=(
            ("INCREASE", "Increase", "Raise Subdivision Level"),
            ("DECREASE", "Decrease", "Lower Subdivision Level"),
        ),
        name='Increase/Decrease',
        description='Raise/Lower Subdivision Level',
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and "SCULPT" in context.mode

    def invoke(self, context, event):
        self.obj = context.active_object
        self.mods = [mod for mod in self.obj.modifiers if mod.type == "MULTIRES"]
        if not self.mods:
            bpy.ops.object.modifier_add(type="MULTIRES")
            self.mod = self._get_last_modifier()
        else:
            self.mod = self.mods[0]
        if "SCULPT" in context.mode:
            self.current_level = self.mod.sculpt_levels
        else:
            self.current_level = self.mod.levels
        self.num_levels = self.mod.total_levels
        return self.execute(context)

    def execute(self, context):
        addend = 1
        if self.inc_dec == "DECREASE":
            addend = -1
        val = self.current_level + addend
        new_level = utils.clamp(val, 0, 6)
        if self.num_levels == self.current_level and self.inc_dec == "INCREASE":
            bpy.ops.object.multires_subdivide(modifier=self.mod.name)
        else:
            self.mod.levels = new_level
            self.mod.sculpt_levels = new_level
        return {"FINISHED"}
    
kms = [
    {
        "keymap_operator": SCULPT_OT_change_multires_subdiv_level.bl_idname,
        "name": "Sculpt",
        "letter": "NUMPAD_PLUS",
        "shift": 1,
        "ctrl": 1,
        "alt": 1,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"inc_dec": "INCREASE"},
    },
    {
        "keymap_operator": SCULPT_OT_change_multires_subdiv_level.bl_idname,
        "name": "Sculpt",
        "letter": "NUMPAD_MINUS",
        "shift": 1,
        "ctrl": 1,
        "alt": 1,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"inc_dec": "DECREASE"},
    },
]