# import bpy
# from bpy.types import Menu

# COLOR_TYPES = ["MATERIAL", "SINGLE", "OBJECT", "RANDOM", "VERTEX", "TEXTURE"]

# class VIEW3D_MT_PIE_display_options(Menu):
#     bl_label = "Display Type"
#     bl_idname = "VIEW3D_MT_PIE_display_options"

#     @classmethod
#     def poll(cls, context):
#         return context.active_object is not None

#     def draw(self, context):
#         layout = self.layout
#         pie = layout.menu_pie()
#         for ct in COLOR_TYPES:
#             prop = pie.prop(context.area.screen.shading, "color_type")


# kms = [
#     {
#         "keymap_operator": "wm.call_menu_pie",
#         "name": "Object Mode",
#         "letter": "THREE",
#         "shift": 0,
#         "ctrl": 1,
#         "alt": 1,
#         "space_type": "VIEW_3D",
#         "region_type": "WINDOW",
#         "keywords": {"name": VIEW3D_MT_PIE_display_options.bl_idname},
#     }
# ]
