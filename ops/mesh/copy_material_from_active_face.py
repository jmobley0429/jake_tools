
import bpy
import bmesh
import bmesh_utils
from custom_operator import *

def assign_material_from_active(context):
    mesh = context.edit_object.data
    bm = bmesh_utils.get_bmesh(context)
    ami = bm.faces.active.material_index
    for face in bm.faces[:]:
        if face.select:
            face.material_index = ami 
            face.select_set(False)
        
    bmesh.update_edit_mesh(mesh)


class MESH_OT_assign_material_from_active_face(CustomOperator, bpy.types.Operator):
    bl_idname = "mesh.assign_material_from_active_face"
    bl_label = "Assign Material From Active Face"

    @classmethod
    def poll(cls, context):
        return cls.edit_obj_poll(context)

    def execute(self, context):
        assign_material_from_active(context)
        return {"FINISHED"}
    


