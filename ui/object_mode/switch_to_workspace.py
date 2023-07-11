import bpy
from bpy.types import Menu


class VIEW3D_MT_PIE_switch_to_workspace(Menu):
    # label is displayed at the center of the pie menu.
    bl_idname = "VIEW3D_MT_PIE_switch_to_workspace"
    bl_label = "Switch to Workspace Pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        op = pie.operator("wm.switch_to_workspace", text="Modeling")
        op.ws_type = "Modeling"
        op = pie.operator("wm.switch_to_workspace", text="Geometry Nodes")
        op.ws_type = "Geometry Nodes"
        op = pie.operator("wm.switch_to_workspace", text="Scripting")
        op.ws_type = "Scripting"
        op = pie.operator("wm.switch_to_workspace", text="UV Editing")
        op.ws_type = "UV Editing"
        op = pie.operator("wm.switch_to_workspace", text="Asset Browser")
        op.ws_type = "Asset Browser"
        op = pie.operator("wm.switch_to_workspace", text="Animation")
        op.ws_type = "Animation"
        op = pie.operator("wm.switch_to_workspace", text="Compositing")
        op.ws_type = "Compositing"

        op = pie.operator("wm.switch_to_workspace", text="Shading")
        op.ws_type = "Shading"


kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Window",
        "letter": "ACCENT_GRAVE",
        "shift": 0,
        "ctrl": 0,
        "alt": 1,
        "space_type": "EMPTY",
        "region_type": "WINDOW",
        "keywords": {
            "name": VIEW3D_MT_PIE_switch_to_workspace.bl_idname,
        },
    }
]
