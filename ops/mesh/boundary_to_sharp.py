# edit_mode
from bpy.types import Operator
import bpy
from custom_operator import *


class MESH_OT_boundary_to_sharp(CustomOperator, Operator):
    bl_idname = "mesh.boundary_to_sharp"
    bl_label = "Boundary to Sharp"

    @classmethod
    def poll(cls, context):
        return cls.edit_obj_poll(context)

    def execute(self, context):
        bpy.ops.mesh.region_to_loop()
        bpy.ops.mesh.mark_sharp()
        return {"FINISHED"}
