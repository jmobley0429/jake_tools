from bpy.types import Menu


class PIE_MT_PieCustomDelete(Menu):
    bl_idname = "PIE_MT_PieCustomDelete"
    bl_label = "Pie Delete Elements"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # 4 - LEFT
        box = pie.split().column()

        # box.operator_context = "EXEC_DEFAULT"

        box.operator(
            "mesh.dissolve_limited", text="Limited Dissolve", icon="STICKY_UVS_LOC"
        )
        box.operator(
            "mesh.delete_elements", text="Delete Edge Loops", icon="NONE"
        ).operator_to_call = "mesh.delete_edgeloop"
        box.operator(
            "mesh.delete_elements", text="Edge Collapse", icon="UV_EDGESEL"
        ).operator_to_call = "mesh.edge_collapse"
        # 6 - RIGHT
        box = pie.split().column()
        box.operator(
            "mesh.delete_elements", text="Merge By Distance", icon="NONE"
        ).operator_to_call = "mesh.remove_doubles"
        op = box.operator("mesh.delete_elements", text="Only Edge & Faces", icon="NONE")
        op.del_type = "EDGE_FACE"
        op.operator_to_call = "mesh.delete"
        op = box.operator("mesh.delete_elements", text="Only Faces", icon="UV_FACESEL")
        op.del_type = "ONLY_FACE"
        op.operator_to_call = "mesh.delete"
        # 2 - BOTTOM
        pie.operator(
            "mesh.delete_elements", text="Dissolve Edges", icon="SNAP_EDGE"
        ).operator_to_call = "mesh.dissolve_edges"
        # 8 - TOP
        op = pie.operator(
            "mesh.delete_elements",
            text="Delete Edges",
            icon="EDGESEL",
        )
        op.del_type = "EDGE"
        op.operator_to_call = "mesh.delete"
        # 7 - TOP - LEFT
        op = pie.operator(
            "mesh.delete_elements", text="Delete Vertices", icon="VERTEXSEL"
        )
        op.del_type = "VERT"
        op.operator_to_call = "mesh.delete"
        # 9 - TOP - RIGHT
        op = pie.operator("mesh.delete_elements", text="Delete Faces", icon="FACESEL")
        op.del_type = "FACE"
        op.operator_to_call = "mesh.delete"
        # 1 - BOTTOM - LEFT
        pie.operator(
            "mesh.delete_elements", text="Dissolve Vertices", icon="SNAP_VERTEX"
        ).operator_to_call = "mesh.dissolve_verts"
        # 3 - BOTTOM - RIGHT
        pie.operator(
            "mesh.delete_elements", text="Dissolve Faces", icon="SNAP_FACE"
        ).operator_to_call = "mesh.dissolve_faces"


kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Mesh",
        "letter": "X",
        "shift": 0,
        "ctrl": 0,
        "alt": 0,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": PIE_MT_PieCustomDelete.bl_idname},
    }
]
