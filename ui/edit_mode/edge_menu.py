from bpy.types import Menu

from jake_tools.ops.mesh.collapse_edges_to_vert import MESH_OT_collapse_edges_to_vert
from jake_tools.ops.mesh.select_boundary import MESH_OT_select_boundary_loops
from jake_tools.ops.mesh.auto_mark_sharp_edges import MESH_OT_auto_mark_sharp


class MESH_MT_edge_menu(Menu):
    # label is displayed at the center of the pie menu.
    bl_idname = "MESH_MT_edge_menu"
    bl_label = "Edge Menu"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # Left
        col = pie.split().column()
        op = col.operator("mesh.mark_seam", text="Mark Seam")
        op = col.operator("mesh.mark_seam", text="Clear Seam")
        op.clear = True
        col.operator("mesh.boundary_to_seam", text="Boundary to Seam")
        # Right bevel weights
        col = pie.split().column()
        op = col.operator("mesh.toggle_edge_weight", text="Toggle Bevel Weight")
        op.weight_type = "BEVEL"
        op = col.operator("mesh.set_sharp_to_weighted", text="Sharp to Beveled")
        op.weight_type = "BEVEL"
        op = col.operator("mesh.set_boundary_to_weighted", text="Boundary to Beveled")
        op.weight_type = "BEVEL"
        # Bottom - Select Edge loops/rings
        bx = pie.split().box()
        bx.label(text="Select Edges")
        bx.ui_units_y -= 50
        col = bx.column()
        col.operator("mesh.loop_multi_select", text="Edge Rings").ring = True
        col.operator("mesh.loop_multi_select", text="Edge Loops").ring = False
        col.operator("mesh.select_nth")
        row = col.row(align=True)
        row.operator("mesh.subdivide_inner_edges")
        row = col.row(align=True)
        row.operator(MESH_OT_collapse_edges_to_vert.bl_idname)
        # Top select sharp, regions etc.
        bx = pie.split().box()
        bx.label(text="Select")
        col = bx.column()
        col.operator("mesh.edges_select_sharp", text="Sharp Edges")
        col.operator("mesh.loop_to_region", text="Inner Region")
        col.operator(MESH_OT_select_boundary_loops.bl_idname, text="Boundary Loop")
        # TOP LEFT - set sharps
        col = pie.split().column()
        col.operator(MESH_OT_auto_mark_sharp.bl_idname, text="Auto Mark Sharp")
        op = col.operator("mesh.mark_sharp", text="Clear Sharp")
        op.clear = True
        col.operator("mesh.boundary_to_sharp")
        #
        col = pie.split().column()
        col.operator("mesh.increase_cylinder_res")
        col.operator("mesh.reduce_cylinder")
        col.operator("mesh.reduce_circle_segments")
        #
        # Right
        col = pie.split().column()
        op = col.operator("mesh.toggle_edge_weight", text="Toggle Crease")
        op.weight_type = "CREASE"
        op = col.operator("mesh.set_sharp_to_weighted", text="Sharp to Creased")
        op.weight_type = "CREASE"
        op = col.operator("mesh.set_boundary_to_weighted", text="Boundary to Creased")
        op.weight_type = "CREASE"

        # Bottom
        col = pie.split().column()
        col.ui_units_x += 5
        row = col.row(align=True)
        row.operator("mesh.edge_split")
        row = col.row(align=True)
        spl = row.split()
        spl.operator("mesh.edge_rotate", text="Rotate CW").use_ccw = False
        spl.operator("mesh.edge_rotate", text="CCW").use_ccw = True
        row = col.row(align=True)
        row.operator("mesh.offset_edge_loops_slide")


kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Mesh",
        "letter": "E",
        "shift": True,
        "ctrl": True,
        "alt": False,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": MESH_MT_edge_menu.bl_idname},
    }
]
