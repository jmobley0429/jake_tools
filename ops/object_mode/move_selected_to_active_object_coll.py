import bpy


def main(context, op):
    sel_objs = context.selected_objects
    ao = context.active_object
    ao_coll = ao.users_collection[0]
    for obj in sel_objs:
        if obj is not ao:
            obj_coll = obj.users_collection[0]
            if obj_coll is not ao_coll:
                ao_coll.objects.link(obj)
                obj_coll.objects.unlink(obj)
    return {"FINISHED"}


class OBJECT_OT_move_selected_to_active_object_coll(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "object.move_selected_to_active_object_coll"
    bl_label = "Move Selected to Active Object's Collection"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and len(context.selected_objects) > 1

    def execute(self, context):

        return main(context, self)
