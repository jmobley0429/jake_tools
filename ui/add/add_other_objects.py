from bpy.types import Menu


class PIE_MT_AddOtherObjects(Menu):
    bl_idname = "PIE_MT_AddOtherObjects"
    bl_label = "Pie Add Other Objects"

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
            "object.lightprobe_add", text="Irradiance Volume", icon="LIGHTPROBE_VOLUME"
        )
        op.type = "VOLUME"
        spl = box.split()
        op = spl.operator(
            "object.lightprobe_add", text="Cube", icon="LIGHTPROBE_SPHERE"
        )
        op.type = "SPHERE"
        op = spl.operator(
            "object.lightprobe_add", text="Plane", icon="LIGHTPROBE_PLANE"
        )
        op.type = "PLANE"
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
        box = pie.split().column()
        box.label(text="Grease Pencil")
        spl = box.split()
        op = spl.operator("object.gpencil_add", text="Blank", icon="EMPTY_AXIS")
        op.type = "EMPTY"
        op = spl.operator(
            "object.gpencil_add", text="Stroke", icon="OUTLINER_OB_GREASEPENCIL"
        )
        op.type = "STROKE"
        spl = box.split()
        op = spl.operator(
            "object.gpencil_add", text="Line Art Object", icon="OBJECT_DATA"
        )
        op.type = "LRT_OBJECT"
        spl = box.split()
        op = spl.operator(
            "object.gpencil_add", text="Line Art Collection", icon="OUTLINER_COLLECTION"
        )
        op.type = "LRT_COLLECTION"

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
