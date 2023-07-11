import json
from pathlib import Path

import bpy

from jake_tools.ops.custom_operator import CustomOperator

PARENT_DIR = Path(__file__).parent
file_path = PARENT_DIR / 'mannequin.json'

def _get_mesh_data():
    with open(file_path, 'rb') as f:
        mesh_data = json.load(f)
    mesh = bpy.data.meshes.new("Mannequin")
    mesh.from_pydata(**mesh_data)
    return mesh

def _handle_transforms(obj):
    init_z_dim = obj.dimensions.z
    multiplier = 1.9 / init_z_dim
    obj.dimensions *= multiplier

def _place_in_scene(context, obj):
    bpy.ops.object.select_all(action="DESELECT")
    context.collection.objects.link(obj)
    obj.select_set(True)
    context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    bpy.ops.object.shade_smooth()
    bpy.ops.object.pivotobottom()
    cursor_loc = bpy.context.scene.cursor.location
    obj.location = cursor_loc
    

def add_mannequin(context):
    mesh = _get_mesh_data()
    obj = bpy.data.objects.new(mesh.name, mesh)
    _handle_transforms(obj)
    _place_in_scene(context, obj)

class AddMannequin(CustomOperator, bpy.types.Operator):
    bl_idname = "mesh.primitive_mannequin_add"
    bl_label = "Mannequin"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        add_mannequin(context)
        return {'FINISHED'}
    
