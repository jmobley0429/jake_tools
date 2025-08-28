import bpy
from bpy.types import Menu


OBJECT_DISPLAY_TYPES = ["BOUNDS", "WIRE", "SOLID", "TEXTURED"]
SHADING_COLOR_TYPES = ["MATERIAL", "OBJECT", "RANDOM", "TEXTURE", "VERTEX", "SINGLE"]


class VIEW3D_MT_PIE_display_options(Menu):
    bl_label = "Display Type"
    bl_idname = "VIEW3D_MT_PIE_display_options"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # for _type in OBJECT_DISPLAY_TYPES:
        #     prop = pie.prop(context.object, _type, text=_type.capitalize())
        pie.prop_tabs_enum(context.object, "display_type")
        pie.prop(context.object, "show_in_front")
        box = pie.box()
        prop = box.prop(context.space_data.shading, "color_type")


kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Object Mode",
        "letter": "THREE",
        "shift": 0,
        "ctrl": 1,
        "alt": 1,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": VIEW3D_MT_PIE_display_options.bl_idname},
    }
]
