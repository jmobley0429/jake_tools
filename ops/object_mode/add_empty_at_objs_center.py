import bpy
from bpy.types import Operator
import utils
import numpy as np

class OBJECT_add_empty_at_objs_center(Operator):
    bl_idname = "object.add_empty_at_objs_center"
    bl_label = "Add Object at Objects Center"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def _add_object_and_parent(self, context, obj):
        matrix = obj.matrix_world
        center = utils.get_bbox_center(obj, matrix)
        bpy.ops.object.empty_add(type="SPHERE", location=center)
        empty = context.object
        empty.empty_display_size = 0.25
        utils.set_parent(obj, empty)

    def execute(self, context):
        obj = context.active_object
        objs = context.selected_objects

        if len(objs) > 1:
            centers = []
            for obj in objs:
                mx = obj.matrix_world
                center = utils.get_bbox_center(obj, mx)
                centers.append(center)

            centers = np.array(centers)
            objs_center = np.mean(centers, axis=0)
            bpy.ops.object.empty_add(location=objs_center)
            empty = context.object

            for obj in objs:
                orig_mxt = obj.matrix_world.translation.copy()
                obj.parent = empty
                obj.matrix_world.translation = orig_mxt

        else:
            self._add_object_and_parent(context, obj)

        return {"FINISHED"}
