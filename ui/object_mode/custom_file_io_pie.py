import bpy
import utils
from bpy.types import Menu


class PIE_MT_CustomFileIO(Menu):
    bl_idname = "PIE_MT_CustomFileIO"
    bl_label = "Custom File I/O Pie"

    def draw(self, context):
        layout = self.layout
        ob = context.active_object
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("wm.save_mainfile", text="Save")
        # 6 - RIGHT
        pie.operator("wm.open_mainfile", text="Open", icon="FILE_FOLDER")
        # 2 - BOTTOM
        box = pie.box()
        box.scale_x = 1.25

        row = box.row()
        row.menu("TOPBAR_MT_file_import", icon="IMPORT")
        row = box.row()
        row.menu("TOPBAR_MT_file_export", icon="EXPORT")
        # # 8 - TOP
        pie.menu("TOPBAR_MT_file_new", text="New")
        # # 7 - TOP - LEFT
        pie.operator("wm.save_as_mainfile")
        # # 9 - TOP - RIGHT
        pie.menu("TOPBAR_MT_file_open_recent", text="Open Recent")
        # 1 - BOTTOM - LEFT
        pie.operator("wm.save_mainfile", text="Save Incremental").incremental = True
        # # 1 - BOTTOM - Right
        box = pie.box()
        row = box.row()
        row.operator("wm.revert_mainfile", text="Revert")
        row = box.row()
        row.menu("TOPBAR_MT_file_recover", text="Recover")


kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "3D View",
        "letter": "S",
        "shift": 0,
        "ctrl": 1,
        "alt": 0,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": PIE_MT_CustomFileIO.bl_idname},
    }
]
