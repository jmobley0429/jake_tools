import bpy
import utils
from bpy.types import Menu


class PIE_MT_CustomSwitchObjectMode(Menu):
    bl_idname = "PIE_MT_CustomSwitchObjectMode"
    bl_label = "Custom Switch Object Mode"

    def draw(self, context):
        layout = self.layout
        ob = context.active_object
        pie = layout.menu_pie()

        pie.operator_enum("object.mode_set", "mode")
        # 4 - LEFT
        # op = pie.operator("object.transform_apply", text="Location")
        # op.location = True
        # # 6 - RIGHT
        # op = pie.operator("object.transform_apply", text="Scale")
        # op.scale = True
        # # 2 - BOTTOM
        # op = pie.operator("object.transform_apply", text="Apply All")
        # op.rotation = True
        # op.scale = True
        # op.location = True
        # # 8 - TOP

        # op = pie.operator("object.transform_apply", text="Rotation")
        # op.rotation = True

        # 7 - TOP - LEFT

        # 9 - TOP - RIGHT

        # 1 - BOTTOM - LEFT

        # 1 - BOTTOM - Right


kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "3D View",
        "letter": "TAB",
        "shift": 0,
        "ctrl": 1,
        "alt": 0,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": PIE_MT_CustomSwitchObjectMode.bl_idname},
    }
]
