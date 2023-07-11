from bpy.types import Menu


class PIE_MT_ConvertMeshCurve(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "Convert Mesh/Curve"
    bl_idname = "PIE_MT_ConvertMeshCurve"


    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        op = pie.operator("object.custom_convert_object", text="Curve")
        op.target = "CURVE"
        op = pie.operator("object.custom_convert_object", text="Mesh")
        op.target = "MESH"
        op = pie.operator("object.custom_convert_object", text="Grease Pencil")
        op.target = "GPENCIL"
        op = pie.operator("object.custom_convert_object", text="Curves")
        op.target = "CURVES"

kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Object Mode",
        "letter": "C",
        "shift": 0,
        "ctrl": 0,
        "alt": 1,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": PIE_MT_ConvertMeshCurve.bl_idname},
    }
]
