from bpy.types import Menu


class PIE_MT_AddModifier(Menu):
    bl_idname = "PIE_MT_AddModifier"
    bl_label = "Pie Add Modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        ob = context.object
        return ob and ob.type != 'GPENCIL'

    def draw(self, context):
        obj = context.active_object
        layout = self.layout
        pie = layout.menu_pie()

        # Left -- Mirror
        pie = layout.menu_pie()
        box = pie.split().column()
        box.label(text="Mirror")
        box.scale_x = 1.2
        spl = box.split()
        op = spl.operator('object.custom_mirror_modifier', text="X -", icon="MOD_MIRROR")
        op.mirror_type = "X_POS"
        op = spl.operator('object.custom_mirror_modifier', text="X +", icon="MOD_MIRROR")
        op.mirror_type = "X_NEG"
        spl = box.split()
        op = spl.operator('object.custom_mirror_modifier', text="Y -", icon="MOD_MIRROR")
        op.mirror_type = "Y_POS"
        op = spl.operator('object.custom_mirror_modifier', text="Y +", icon="MOD_MIRROR")
        op.mirror_type = "Y_NEG"
        spl = box.split()
        op = spl.operator('object.custom_mirror_modifier', text="Z -", icon="MOD_MIRROR")
        op.mirror_type = "Z_POS"
        op = spl.operator('object.custom_mirror_modifier', text="Z +", icon="MOD_MIRROR")
        op.mirror_type = "Z_NEG"
        # Right -- Bevel / Shading
        box = pie.split().column()
        box.operator('object.custom_bevel_modifier', text="Bevel", icon="MOD_BEVEL")
        box.operator('object.custom_bevel_subsurf_modifier', text="Bevel Subsurf", icon="MOD_SUBSURF")
        op = box.operator('object.auto_crease_subdivide', text="Auto Crease Subdiv", icon="SNAP_EDGE")

        # Bottom -- Deform
        box = pie.split().column()
        box.operator("object.custom_simple_deform", text="Bend", icon="MOD_SIMPLEDEFORM")
        box.operator("object.custom_displace", text="Displace", icon="MOD_DISPLACE")
        box.operator("object.custom_shrinkwrap", text="Shrinkwrap", icon="MOD_SHRINKWRAP")
        box.operator("object.custom_lattice", text="Lattice", icon="OUTLINER_DATA_LATTICE")
        # Top -- Mesh \ Edges
        box = pie.split().column()
        op = box.operator("object.array_modal", text="Array", icon="MOD_ARRAY")
        box.operator("object.solidify_modal", text="Solidify", icon="MOD_SOLIDIFY")
        box.operator("object.screw_modal", text="Screw", icon="MOD_SCREW")
        # TL --
        op = pie.menu('PIE_MT_PhysicsSubPie', text="Physics", icon='PHYSICS')
        # TR --
        op = pie.menu("PIE_MT_MeshSubPie", text="Mesh", icon='MOD_REMESH')
        # BL --
        op = pie.operator("object.multiple_modifiers_add", text="Geometry Nodes", icon="NODETREE")
        op.mod_type = "NODES"
        # BL --
        op = pie.menu("PIE_MT_NormalSubPie", text="Normals and UVs", icon="SNAP_NORMAL")

kms = [
   {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Object Mode",
        "letter": "Q",
        "shift": 1,
        "ctrl": 1,
        "alt": 0,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": PIE_MT_AddModifier.bl_idname},
    },
]