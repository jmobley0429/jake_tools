# edit_mode
import bpy
import bmesh
from bpy.types import Operator
from custom_operator import *


class MESH_OT_weld_verts_to_active(Operator):

    """Weld all selected verts to active vertex."""

    bl_idname = "mesh.weld_verts_to_active"
    bl_label = "Weld to Active"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == "MESH" and "EDIT" in context.mode

    def execute(self, context):
        try:
            bpy.ops.view3d.snap_selected_to_active()
            bpy.ops.mesh.remove_doubles(use_unselected=True)
        except RuntimeError:
            bpy.ops.mesh.merge(type="CENTER")
        return {"FINISHED"}
