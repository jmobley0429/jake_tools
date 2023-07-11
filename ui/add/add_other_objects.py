from bpy.types import Menu


class PIE_MT_AddOtherObjects(Menu):
    bl_idname = "PIE_MT_AddOtherObjects"
    bl_label = "Pie Add Other Objects"
    bl_options = {"REGISTER", "UNDO"}

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # Left -- Lights
        box = pie.split().column()
        box.label(text="Light")
        spl = box.split()
        op = spl.operator("object.custom_light_add", text="Point", icon="LIGHT_POINT")
        op.light_type = "POINT"
        op = spl.operator("object.custom_light_add", text="Area", icon="LIGHT_AREA")
        op.light_type = "AREA"
        spl = box.split()
        op = spl.operator("object.custom_light_add", text="Sun", icon="LIGHT_SUN")
        op.light_type = "SUN"
        op = spl.operator("object.custom_light_add", text="Spot", icon="LIGHT_SPOT")
        op.light_type = "SPOT"
        # Right -- CubeMaps
        box = pie.split().column()
        box.label(text="Light Probes")
        op = box.operator(
            "object.lightprobe_add", text="Irradiance Volume", icon="LIGHTPROBE_GRID"
        )
        op.type = "GRID"
        spl = box.split()
        op = spl.operator(
            "object.lightprobe_add", text="Cube", icon="LIGHTPROBE_CUBEMAP"
        )
        op.type = "CUBEMAP"
        op = spl.operator(
            "object.lightprobe_add", text="Plane", icon="LIGHTPROBE_PLANAR"
        )
        op.type = "PLANAR"
        # Bottom -- Camera
        pie.operator("object.smart_add_camera", text="Add Camera", icon="CAMERA_DATA")

        # Top -- Images as Planes
        pie.operator("import_image.to_plane", text="Image as Plane", icon="FILE_IMAGE")
        # Text
        pie.operator("object.text_add", text="Text", icon="SMALL_CAPS")
        # Mannequin
        pie.operator(
            "mesh.primitive_mannequin_add",
            text="Mannequin",
            icon="OUTLINER_OB_ARMATURE",
        )
        # Armature
        pie.menu("PIE_MT_add_armature_extended", text="Armature", icon="ARMATURE_DATA")
        # Metaball
        
        kms = [
            {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Object Mode",
        "letter": "A",
        "shift": 1,
        "ctrl": 1,
        "alt": 0,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": PIE_MT_AddOtherObjects.bl_idname},
    }
        ]
