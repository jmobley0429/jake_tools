import bpy
import utils
from bpy.types import Menu


class PIE_MT_CustomSetObjectOrigin(Menu):
    bl_idname = "PIE_MT_CustomSetObjectOrigin"
    bl_label = "Custom Set Object Origin"

    def draw(self, context):
        layout = self.layout
        ob = context.active_object
        pie = layout.menu_pie()

        # 4 - LEFT
        op = pie.operator("object.custom_origin_set", text="Origin to Geometry")
        op.type = "ORIGIN_GEOMETRY"
        # 6 - RIGHT
        op = pie.operator("object.custom_origin_set", text="Origin to Cursor")
        op.type = "ORIGIN_CURSOR"
        # 2 - BOTTOM
        pie.operator("object.set_pivot_to_bottom", text="Origin to Bottom")
        # 8 - TOP
        box = pie.box()
        box.label(text="Center of Mass")
        row = box.row()
        spl = row.split()
        op = spl.operator("object.custom_origin_set", text="Surface")
        op.type = "ORIGIN_CENTER_OF_MASS"
        op = spl.operator("object.custom_origin_set", text="Volume")
        op.type = "ORIGIN_CENTER_OF_VOLUME"

        # 7 - TOP - LEFT
        pie.operator(
            "mesh.set_origin_to_edit_mode_selection", text="Origin to Selection"
        )
        # 9 - TOP - RIGHT
        op = pie.operator("object.custom_origin_set", text="Geometry to Origin")
        op.type = "GEOMETRY_ORIGIN"
        # 1 - BOTTOM - LEFT
        # 1 - BOTTOM - Right


kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "3D View",
        "letter": "X",
        "shift": 0,
        "ctrl": 1,
        "alt": 1,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": PIE_MT_CustomSetObjectOrigin.bl_idname},
    }
]
