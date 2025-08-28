import bpy
import utils
from bpy.types import Menu

DEFAULT_ARGS = {
    "location": False,
    "rotation": False,
    "scale": False,
}


def set_operator_args(op, args):
    attrs = "location rotation scale".split()
    for attr in attrs:
        val = attr in args
        setattr(op, attr, val)


class PIE_MT_CustomApplyTransform(Menu):
    bl_idname = "PIE_MT_CustomApplyTransform"
    bl_label = "Custom Apply Transform Pie Menu"

    def draw(self, context):
        layout = self.layout
        ob = context.active_object
        pie = layout.menu_pie()
        # 4 - LEFT
        op = pie.operator("object.transform_apply", text="Location")
        set_operator_args(op, ["location"])
        # 6 - RIGHT
        op = pie.operator("object.transform_apply", text="Scale")
        set_operator_args(op, ["scale"])
        # 2 - BOTTOM
        op = pie.operator("object.transform_apply", text="Apply All")
        args = ["rotation", "scale", "location"]
        set_operator_args(op, args)
        # 8 - TOP
        op = pie.operator("object.transform_apply", text="Rotation")
        set_operator_args(op, ["rotation"])
        # 7 - TOP - LEFT

        # 9 - TOP - RIGHT

        # 1 - BOTTOM - LEFT

        # 1 - BOTTOM - Right


kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Object Mode",
        "letter": "A",
        "shift": 0,
        "ctrl": 1,
        "alt": 0,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": PIE_MT_CustomApplyTransform.bl_idname},
    }
]
