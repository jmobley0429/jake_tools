from bpy.types import Menu
import numpy as np


class MESH_MT_face_menu(Menu):
    # label is displayed at the center of the pie menu.
    bl_idname = "MESH_MT_face_menu"
    bl_label = "Face Pie Menu"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # Left

        op = pie.operator("mesh.faces_select_linked_flat")
        op.sharpness = np.radians(25)
        op = pie.operator("mesh.beautify_fill")
        op = pie.operator("mesh.quads_convert_to_tris")
        box = pie.box()
        box.scale_x *= 0.5
        col = box.column()
        row = col.row()
        spl = row.split()
        spl.operator("mesh.vert_connect_concave")
        spl.operator("mesh.vert_connect_nonplanar")
        row = col.row()
        spl = row.split()
        spl.operator("mesh.fill_holes")
        spl.operator("mesh.face_make_planar")
        row = col.row()
        row.operator("mesh.knife_project")

        col = pie.column()
        op = col.operator("mesh.bisect")
        op = col.operator("mesh.intersect_boolean")
        col = pie.column()
        op = col.operator("mesh.poke")
        op = col.operator("mesh.poke_hole_in_faces")
        pie.operator("mesh.solidify")
        pie.operator_context = "INVOKE_REGION_WIN"
        pie.operator("mesh.smart_grid_fill")


kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Mesh",
        "letter": "F",
        "shift": 1,
        "ctrl": 0,
        "alt": 1,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": MESH_MT_face_menu.bl_idname},
    }
]
