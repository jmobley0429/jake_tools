from bpy.types import Menu


class MESH_MT_PIE_symmetrize(Menu):
    bl_label = "Select Mode"
    bl_idname = "MESH_MT_PIE_symmetrize"
    bl_options = {"REGISTER", "UNDO"}

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator_enum("mesh.symmetrize", "direction")

kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Mesh",
        "letter": "Q",
        "shift": True,
        "ctrl": False,
        "alt": False,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": MESH_MT_PIE_symmetrize.bl_idname},
    }
]