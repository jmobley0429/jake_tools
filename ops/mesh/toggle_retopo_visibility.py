from bpy.types import Operator
from custom_operator import *


def toggle_retopo_visibility(context):
    sd = context.space_data
    obj = context.object
    hidden_wire = sd.show_occlude_wire
    in_front = obj.show_in_front
    wire = obj.show_wire
    overlays = [hidden_wire, in_front, wire]

    toggled = all(overlays)
    for ol in overlays:
        ol = toggled


class MESH_toggle_retopo_visibility(Operator):
    bl_idname = "mesh.toggle_retopo_visibility"
    bl_label = "Toggle Retopo View"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        toggle_retopo_visibility(context)
        return {"FINISHED"}
