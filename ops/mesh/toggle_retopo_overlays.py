# edit_mode

from bpy.types import Operator
from custom_operator import *


def toggle_retopo_overlays(context):
    obj = context.object
    overlay_attrs = ["show_in_front", "show_wire", "show_all_edges"]
    overlay_vals = [getattr(obj, attr) for attr in overlay_attrs]
    is_retopo_view = any(overlay_vals)
    toggle_val = not is_retopo_view
    for attr in overlay_attrs:
        setattr(obj, attr, toggle_val)
    context.space_data.shading.light = "MATCAP"
    context.space_data.shading.color_type = "OBJECT"
    if toggle_val:
        obj.color = [0.000000, 0.650000, 1.000000, 0.500000]
    else:
        obj.color = [1.000000, 1.000000, 1.000000, 1.000000]


class MESH_OT_toggle_retopo_overlays(Operator):
    bl_idname = "mesh.toggle_retopo_overlays"
    bl_label = "Toggle Retopo Views"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        toggle_retopo_overlays(context)
        return {"FINISHED"}
