import bpy
import utils
from custom_operator import *


def move_bool_objects():
    bool_coll = utils.get_or_create_collection("bools")
    bool_objs = bool_coll.objects[:]
    for obj in bpy.data.objects[:]:
        if obj.type == "MESH":
            for mod in obj.modifiers:
                if mod.type == "BOOLEAN" and mod.object is not None:
                    bool_obj = mod.object
                    if bool_obj not in bool_objs:
                        coll = bool_obj.users_collection[0]
                        coll.objects.unlink(bool_obj)
                        bool_coll.objects.link(bool_obj)



class OBJECT_OT_move_bool_objs_to_coll(bpy.types.Operator):
    bl_idname = "object.move_bool_objects_to_coll"
    bl_label = "Move Bool Objects"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT" 
    
    def execute(self, context):
        move_bool_objects()
        return {"FINISHED"}
