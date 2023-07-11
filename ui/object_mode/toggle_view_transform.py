from bpy.types import Menu


class VIEW3D_MT_PIE_toggle_view_transform(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "Toggle View Transform"
    bl_idname = "VIEW3D_MT_PIE_toggle_view_transform"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        # operator_enum will just spread all available options
        # for the type enum of the operator on the pie
        pie.prop_enum(context.scene.view_settings, "view_transform", "Filmic")
        pie.prop_enum(context.scene.view_settings, "view_transform", "False Color")


kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Object Mode",
        "letter": "V",
        "shift": 0,
        "ctrl": 0,
        "alt": 1,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": VIEW3D_MT_PIE_toggle_view_transform.bl_idname},
    }
]
