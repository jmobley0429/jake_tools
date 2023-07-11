import bpy
from bpy.types import Menu

class MESH_MT_merge_verts_pie(Menu):
    bl_idname = 'MESH_MT_merge_verts_pie'
    bl_label = "Merge Verts"
    bl_options = {"REGISTER", "UNDO"}

    def draw(self, _context):
        layout = self.layout
        pie = layout.menu_pie()

        op = pie.operator('mesh.merge', text="Center")
        op.type = "CENTER"
        op = pie.operator('mesh.merge', text="Collapse")
        op.type = "COLLAPSE"
        pie.operator('mesh.weld_verts_to_active', text="Active")
        op = pie.operator('mesh.remove_doubles', text="Remove Doubles")
        op.use_unselected = True

kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Mesh",
        "letter": "W",
        "shift": 1,
        "ctrl": 0,
        "alt": 0,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": MESH_MT_merge_verts_pie.bl_idname},
    }
]