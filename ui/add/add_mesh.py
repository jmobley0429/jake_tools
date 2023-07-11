import bpy
from bpy.types import Menu

class PIE_MT_AddMesh(Menu):
    bl_idname = "PIE_MT_AddMesh"
    bl_label = "Pie Add Mesh"
    bl_options = {"REGISTER", "UNDO"}

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        box = pie.split().column()
        # Left -- Cube
        spl = box.split()
        op = spl.operator("mesh.custom_cube_add", text="1m", icon="MESH_CUBE")
        op.size = 1
        op = spl.operator("mesh.custom_cube_add", text="10m", icon="MESH_CUBE")
        op.size = 10
        spl = box.split()
        op = spl.operator("mesh.custom_cube_add", text=".5m", icon="MESH_CUBE")
        op.size = 0.5
        op = spl.operator("mesh.custom_cube_add", text="5m", icon="MESH_CUBE")
        op.size = 5
        spl = box.split()
        op = spl.operator("mesh.custom_cube_add", text=".25m", icon="MESH_CUBE")
        op.size = 0.25
        op = spl.operator("mesh.custom_cube_add", text="2m", icon="MESH_CUBE")
        op.size = 2

        # Right -- Sphere
        col = pie.column()
        spl = col.split()
        op = spl.operator("mesh.primitive_uv_sphere_add", text="UV - 32", icon="MESH_UVSPHERE")
        op.segments = 32
        op.ring_count = 16
        op.radius = 1
        op = spl.operator("mesh.primitive_uv_sphere_add", text="UV - 16", icon="MESH_UVSPHERE")
        op.segments = 16
        op.ring_count = 8
        op.radius = 1
        spl = col.split()
        op = spl.operator("mesh.primitive_ico_sphere_add", text="Ico - 2", icon="MESH_ICOSPHERE")
        op.subdivisions = 2
        op = spl.operator("mesh.primitive_ico_sphere_add", text="Ico - 1", icon="MESH_ICOSPHERE")
        op.subdivisions = 2
        spl = col.split()
        op = spl.operator("mesh.primitive_round_cube_add", text="Quad - 8", icon="MESH_UVSPHERE")
        op.arc_div = 8
        op.radius = 1
        op.div_type = "CORNERS"
        op = spl.operator("mesh.primitive_round_cube_add", text="Quad - 4", icon="MESH_UVSPHERE")
        op.arc_div = 4
        op.radius = 1
        op.div_type = "CORNERS"

        # bottom -- Circle
        box = pie.split().column()
        spl = box.split()
        op = spl.operator("mesh.primitive_circle_add", text="6", icon="MESH_CIRCLE")
        op.vertices = 6
        op.radius = 0.125
        op = spl.operator("mesh.primitive_circle_add", text="12", icon="MESH_CIRCLE")
        op.vertices = 12
        op.radius = 0.125
        spl = box.split()
        op = spl.operator("mesh.primitive_circle_add", text="8", icon="MESH_CIRCLE")
        op.vertices = 8
        op.radius = 0.125
        op = spl.operator("mesh.primitive_circle_add", text="16", icon="MESH_CIRCLE")
        op.vertices = 16
        op.radius = 0.125
        spl = box.split()
        op = spl.operator("mesh.primitive_circle_add", text="24", icon="MESH_CIRCLE")
        op.vertices = 24
        op.radius = 0.125
        op = spl.operator("mesh.primitive_circle_add", text="48", icon="MESH_CIRCLE")
        op.vertices = 48
        op.radius = 0.125
        spl = box.split()
        op = spl.operator("mesh.primitive_circle_add", text="32", icon="MESH_CIRCLE")
        op.vertices = 32
        op.radius = 0.125
        op = spl.operator("mesh.primitive_circle_add", text="64", icon="MESH_CIRCLE")
        op.vertices = 64
        op.radius = 0.125

        # Top -- Cylinder
        box = pie.split().column()
        box.ui_units_y -= 25
        spl = box.split()
        op = spl.operator("mesh.custom_cylinder_add", text="6", icon="MESH_CYLINDER")
        op.vertices = 6
        op = spl.operator("mesh.custom_cylinder_add", text="12", icon="MESH_CYLINDER")
        op.vertices = 12
        spl = box.split()
        op = spl.operator("mesh.custom_cylinder_add", text="8", icon="MESH_CYLINDER")
        op.vertices = 8
        op = spl.operator("mesh.custom_cylinder_add", text="16", icon="MESH_CYLINDER")
        op.vertices = 16
        spl = box.split()
        op = spl.operator("mesh.custom_cylinder_add", text="24", icon="MESH_CYLINDER")
        op.vertices = 24
        op = spl.operator("mesh.custom_cylinder_add", text="48", icon="MESH_CYLINDER")
        op.vertices = 48
        spl = box.split()
        op = spl.operator("mesh.custom_cylinder_add", text="32", icon="MESH_CYLINDER")
        op.vertices = 32
        op = spl.operator("mesh.custom_cylinder_add", text="64", icon="MESH_CYLINDER")
        op.vertices = 64

        box = pie.split().column()
        spl = box.split()
        op = spl.operator("mesh.primitive_plane_add", text="Plane 1m", icon="MESH_PLANE")
        op.size = 1
        op = spl.operator("mesh.primitive_plane_add", text="Plane .5m", icon="MESH_PLANE")
        op.size = 0.5
        spl = box.split()
        op = spl.operator("mesh.primitive_grid_add", text="Grid 25", icon="MESH_GRID")
        op.x_subdivisions = 25
        op.y_subdivisions = 25
        op = spl.operator("mesh.primitive_grid_add", text="Grid 10", icon="MESH_GRID")
        spl = box.split()
        op = spl.operator("mesh.primitive_round_cube_add", text="3D Grid", icon="GRID")
        op.radius = 0.0
        op.lin_div = 5
        op.div_type = "ALL"
        op = spl.operator("mesh.primitive_vert_add", text="Single Vert", icon="DECORATE")

        # Planes
        # empty / other
        box = pie.split().column()
        box.ui_units_y -= 5
        box.ui_units_x -= 5
        spl = box.split()
        op = spl.operator("object.empty_add", text="Plain Axes", icon="EMPTY_AXIS")
        op.type = "PLAIN_AXES"
        op = spl.operator("object.empty_add", text="Arrows", icon="EMPTY_ARROWS")
        op.type = "ARROWS"
        spl = box.split()
        op = spl.operator("object.empty_add", text="Cube", icon="CUBE")
        op.type = "CUBE"
        op = spl.operator("object.empty_add", text="Circle", icon="MESH_CIRCLE")
        op.type = "CIRCLE"
        spl = box.split()
        op = spl.operator("object.empty_add", text="Sphere", icon="CUBE")
        op.type = "SPHERE"
        has_collections = len(bpy.data.collections) > 0
        if has_collections or len(bpy.data.collections) > 10:
            col = box
            spl.operator_context = "INVOKE_REGION_WIN"
            spl.operator(
                "object.collection_instance_add",
                text="Collection" if has_collections else "No Collections",
                icon="OUTLINER_OB_GROUP_INSTANCE",
            )
        else:
            spl.operator_menu_enum(
                "object.collection_instance_add",
                "collection",
                text="Collection Instance",
                icon="OUTLINER_OB_GROUP_INSTANCE",
            )

        # Random
        box = pie.split().column()
        box.ui_units_y += 2
        op = box.operator("mesh.primitive_torus_add", text="Torus", icon="MESH_TORUS")
        op = box.operator("mesh.primitive_cone_add", text="Cone", icon="MESH_CONE")
        op = box.operator("mesh.primitive_monkey_add", text="Monkey", icon="MESH_MONKEY")

        # Curves
        box = pie.split().column()
        box.ui_units_y += 2
        op = box.operator("curve.primitive_bezier_curve_add", text="Bezier Curve", icon="IPO_BEZIER")
        op = box.operator("curve.primitive_nurbs_path_add", text="Path", icon="CURVE_PATH")
        op = box.operator("curve.primitive_bezier_circle_add", text="Curve Circle", icon="CURVE_NCIRCLE")


kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Object Mode",
        "letter": "A",
        "shift": 1,
        "ctrl": 0,
        "alt": 0,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": PIE_MT_AddMesh.bl_idname},
    }
]