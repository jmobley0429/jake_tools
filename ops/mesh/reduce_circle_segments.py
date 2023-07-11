import bpy
from bpy.types import Menu



import bpy
from bpy.types import Operator
from custom_operator import *

class MESH_OT_reduce_circle_segments(CustomOperator, Operator):
    """Cut cylinder edges in half, select one edge ring and then execute."""

    bl_idname = "mesh.reduce_circle_segments"
    bl_options = {"REGISTER", "UNDO"}
    bl_label = "Reduce Circle Segments"

    @classmethod
    def poll(cls, context):
        return cls.edit_obj_poll(context)

    def execute(self, context):
        select_vals = context.tool_settings.mesh_select_mode
        select_modes = "VERT EDGE FACE".split()
        bpy.ops.mesh.select_mode(
            use_extend=False, use_expand=False, type='EDGE')
        bpy.ops.mesh.loop_multi_select(ring=False)
        bpy.ops.mesh.select_nth()
        bpy.ops.mesh.merge(type='COLLAPSE')
        for val, mode in zip(select_vals, select_modes):
            if val:
                bpy.ops.mesh.select_mode(
                    use_extend=True, use_expand=False, type=mode)

        return {'FINISHED'}