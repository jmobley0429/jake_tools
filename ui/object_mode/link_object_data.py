import bpy
from bpy.types import Menu

class VIEW3D_MT_PIE_link_object_data(Menu):
    # label is displayed at the center of the pie menu.
    bl_idname = "VIEW3D_MT_PIE_link_object_data"
    bl_label = "Link Data"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # operator_enum will just spread all available options
        # for the type enum of the operator on the pie
        op = pie.operator("object.make_links_data", text="Materials")
        op.type = "MATERIAL"
        op = pie.operator("object.make_links_data", text="Object Data")
        op.type = "OBDATA"
        op = pie.operator("object.make_links_data", text="Modifiers")
        op.type = "MODIFIERS"
        op = pie.operator("object.join_uvs", text="UV Maps")
        layout.operator_context = "EXEC_DEFAULT"
        op = pie.operator("object.make_single_user", text="Make Single User")
        op.obdata = True





kms = [
   {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Object Mode",
        "letter": "FOUR",
        "shift": 0,
        "ctrl": 0,
        "alt": 1,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": VIEW3D_MT_PIE_link_object_data.bl_idname},
    } 
]