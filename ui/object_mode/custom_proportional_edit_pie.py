import bpy
from bpy.types import Menu

# spawn an edit mode selection pie (run while object is in edit mode to get a valid output)


class VIEW3D_MT_PIE_custom_proportional_edit(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "Proportional Edit"
    bl_idname = "VIEW3D_MT_PIE_custom_proportional_edit"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        # operator_enum will just spread all available options
        # for the type enum of the operator on the pie
        pie.prop_tabs_enum(context.scene.tool_settings, "proportional_edit_falloff")


kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "3D View",
        "letter": "O",
        "shift": 1,
        "ctrl": 0,
        "alt": 0,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": VIEW3D_MT_PIE_custom_proportional_edit.bl_idname},
    }
]
