import bpy
from bpy.types import Menu

from jake_tools.ops.mesh.cleanup_mesh import (
    MESH_OT_cleanup_select_short_edges,
    MESH_OT_cleanup_select_small_faces,
    MESH_OT_cleanup_handle_ngons,
)


class MESH_MT_PIE_select_by_trait(Menu):
    bl_label = "Select by Trait"
    bl_idname = "MESH_MT_PIE_select_by_trait"
    bl_options = {"REGISTER", "UNDO"}

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("mesh.select_face_by_sides")
        pie.operator("mesh.select_interior_faces")
        pie.operator("mesh.select_loose")
        pie.operator("mesh.select_non_manifold")
        pie.operator(MESH_OT_cleanup_select_short_edges.bl_idname)
        pie.operator(MESH_OT_cleanup_select_short_edges.bl_idname)
        pie.operator(MESH_OT_cleanup_select_small_faces.bl_idname)
        pie.operator(MESH_OT_cleanup_handle_ngons.bl_idname)

kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Mesh",
        "letter": "TWO",
        "shift": 0,
        "ctrl": 0,
        "alt": 1,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": MESH_MT_PIE_select_by_trait.bl_idname},
    }
]
