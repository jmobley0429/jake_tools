import bpy
import utils
from custom_operator import *

def move_bool_objects(context):
    bool_coll = utils.get_or_create_collection("bools")
    for obj in context.selected_objects:
        coll = utils.find_objects_collection(obj)
        if obj.display_type == "BOUNDS":
            coll.objects.unlink(obj)
            bool_coll.objects.link(obj)


class OBJECT_OT_move_bool_objs_to_coll(bpy.types.Operator):
    bl_idname = "object.move_bool_objects_to_coll"
    bl_label = "Move Bool Objects"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT" and context.selected_objects

    def execute(self, context):
        move_bool_objects(context)
        return {"FINISHED"}
