import bpy


def main(context, operator):
    C = context
    bool_coll_exists = set_bool_objs_to_hidden(operator)
    if not bool_coll_exists:
        return {"CANCELLED"}
    for obj in C.selected_objects:
        for mod in obj.modifiers:
            if mod.type == "BOOLEAN":
                obj = mod.object
                obj.hide_set(False)
    return {"FINISHED"}


def set_bool_objs_to_hidden(operator):
    if "bools" not in bpy.data.collections:
        operator.report({"WARNING"}, text="No Bool Object Collection!")
        return
    for obj in bpy.data.collections["bools"].objects:
        obj.hide_set(True)
    return True


class MODIFIER_OT_set_bool_obj_visibility(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "modifier.set_bool_obj_visibility"
    bl_label = "Set Bool Object Visibility"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context, self)
        return {"FINISHED"}
