import bpy
import utils
from bpy.types import Menu


class PIE_MT_CustomViewNumpad(Menu):
    bl_idname = "PIE_MT_CustomViewNumpad"
    bl_label = "Custom Views Pie Menu"

    def draw(self, context):
        layout = self.layout
        ob = context.active_object
        pie = layout.menu_pie()
        scene = context.scene
        rd = scene.render

        # 4 - LEFT
        pie.operator("view3d.view_axis", text="Left", icon="TRIA_LEFT").type = "LEFT"
        # 6 - RIGHT
        pie.operator("view3d.view_axis", text="Right", icon="TRIA_RIGHT").type = "RIGHT"
        # 2 - BOTTOM
        pie.operator(
            "view3d.view_axis", text="Bottom", icon="TRIA_DOWN"
        ).type = "BOTTOM"
        # 8 - TOP
        pie.operator("view3d.view_axis", text="Top", icon="TRIA_UP").type = "TOP"
        # 7 - TOP - LEFT
        pie.operator("view3d.view_axis", text="Front").type = "FRONT"
        # 9 - TOP - RIGHT
        pie.operator("view3d.view_axis", text="Back").type = "BACK"
        # 1 - BOTTOM - LEFT
        pie.operator("view3d.localview", text="Local/Global")
        # 1 - BOTTOM - Right
        pie.operator("view3d.view_selected", text="Selected")


kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "3D View",
        "letter": "ACCENT_GRAVE",
        "shift": 0,
        "ctrl": 0,
        "alt": 0,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": PIE_MT_CustomViewNumpad.bl_idname},
    }
]
