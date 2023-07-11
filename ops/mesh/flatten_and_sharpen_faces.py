# edit_mode

from custom_operator import *
import bpy


class MESH_OT_FlattenAndSharpenFaces(CustomOperator, bpy.types.Operator):
    bl_idname = "mesh.flatten_and_sharpen_faces"
    bl_label = "Flatten And Sharpen Faces"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return cls.edit_obj_poll(context)

    def execute(self, context):
        tools = context.scene.tool_settings
        orig_select_mode = tools.mesh_select_mode[:]
        bpy.ops.mesh.edge_face_add()
        bpy.ops.mesh.f2()
        bpy.ops.mesh.face_make_planar()
        bpy.ops.mesh.quads_convert_to_tris(quad_method="BEAUTY", ngon_method="BEAUTY")
        bpy.ops.mesh.tris_convert_to_quads()
        bpy.ops.mesh.region_to_loop()
        bpy.ops.mesh.mark_sharp()
        for i, mode in enumerate(orig_select_mode):
            if i != 2:
                tools.mesh_select_mode[i] = False
            else:
                tools.mesh_select_mode[i] = True
        return {"FINISHED"}
