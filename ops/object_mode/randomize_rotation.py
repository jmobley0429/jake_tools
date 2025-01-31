import bpy
from mathutils import Vector
import numpy as np


def selected_objects_generator(context):
    for obj in context.selected_objects:
        yield obj


def randomize_rotation(obj):
    rand_rot = Vector([np.random.rand() * 360 for i in range(3)])
    obj.rotation_euler = rand_rot


class OBJECT_OT_randomize_rotation(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "object.randomize_rotation"
    bl_label = "Randomize Rotation"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.selected_objects

    def execute(self, context):
        for obj in selected_objects_generator(context):
            randomize_rotation(obj)
        return {"FINISHED"}
