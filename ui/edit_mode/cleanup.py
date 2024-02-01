from bpy.types import Menu


class MESH_MT_PIE_cleanup(Menu):
    bl_label = "Clean Up Pie"
    bl_idname = "MESH_MT_PIE_cleanup"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        op = pie.operator("mesh.delete_loose")
        op = pie.operator("mesh.decimate")
        op.ratio = 0.1
        op = pie.operator("mesh.dissolve_degenerate")
        op = pie.operator("mesh.face_make_planar")
        op = pie.operator("mesh.vert_connect_nonplanar")
        op = pie.operator("mesh.vert_connect_concave")


kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Mesh",
        "letter": "THREE",
        "shift": 0,
        "ctrl": 0,
        "alt": 1,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": MESH_MT_PIE_cleanup.bl_idname},
    }
]
