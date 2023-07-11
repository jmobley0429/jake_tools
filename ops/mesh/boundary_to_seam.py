import bpy
from bpy.types import Operator

class MESH_OT_boundary_to_seam(Operator):
    bl_idname = "mesh.boundary_to_seam"
    bl_label = "Boundary to Seam"

    def execute(self, context):
        bpy.ops.mesh.region_to_loop()
        bpy.ops.mesh.mark_seam()
        return {"FINISHED"}