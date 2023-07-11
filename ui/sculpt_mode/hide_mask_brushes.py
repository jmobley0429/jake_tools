import bpy
from bpy.types import Menu


brush_icons = {}


def create_icons():
    global brush_icons

    icons_directory = bpy.utils.system_resource('DATAFILES', path="icons")
    brushes = [
        "border_mask",
        "border_hide",
        "box_trim",
        "line_project",
    ]
    import os

    for brush in brushes:
        icon_str = f"ops.sculpt.{brush}.dat"
        filename = f"{icons_directory}/{icon_str}"
        icon_value = bpy.app.icons.new_triangles_from_file(filename)
        brush_icons[brush] = icon_value


def release_icons():
    global brush_icons
    for value in brush_icons.values():
        bpy.app.icons.release(value)

class PIE_MT_hide_mask_brushes(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "Hide/Mask Brush Menu"
    bl_idname = "PIE_MT_hide_mask_brushes"
    bl_options = {"REGISTER", "UNDO"}

    def draw(self, context):
        global brush_icons
        layout = self.layout

        pie = layout.menu_pie()
        op = pie.operator("wm.tool_set_by_id", text="   Mask", icon_value=brush_icons["border_mask"])
        op.name = "builtin.box_mask"
        op = pie.operator("wm.tool_set_by_id", text="   Hide", icon_value=brush_icons["border_hide"])
        op.name = "builtin.box_hide"
        op = pie.operator("wm.tool_set_by_id", text="   Trim", icon_value=brush_icons["box_trim"])
        op.name = "builtin.box_trim"
        op = pie.operator("wm.tool_set_by_id", text="   Line Project", icon_value=brush_icons["line_project"])
        op.name = "builtin.line_project"


kms = [
{
        "keymap_operator": "wm.call_menu_pie",
        "name": "Sculpt",
        "letter": "TWO",
        "shift": 0,
        "ctrl": 0,
        "alt": 1,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": PIE_MT_hide_mask_brushes.bl_idname},
    },
]

def register():
    create_icons()

def unregister():
    release_icons()