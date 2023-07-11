import bpy
from bpy.types import Menu


import bmesh
import bpy
from bpy.types import Operator
from custom_operator import CustomOperator


class MESH_OT_increase_cylinder_res(CustomOperator, Operator):
    """Double Cylinder Resolution"""

    bl_idname = "mesh.increase_cylinder_res"
    bl_label = "Increase Cylinder Res"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return cls.edit_obj_poll(context)

    def execute(self, context):
        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        bpy.ops.mesh.loop_multi_select(ring=True)
        bpy.ops.mesh.loop_multi_select(ring=False)
        sel_edges = [e for e in bm.edges[:] if e.select]
        bmesh.ops.subdivide_edges(bm, edges=sel_edges, cuts=1)
        bmesh.update_edit_mesh(me)
        bpy.ops.mesh.looptools_circle()
        return {'FINISHED'}