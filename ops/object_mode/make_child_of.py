import bpy


def main(context):
    C = context
    active_obj = C.view_layer.objects.active
    sel_objs = [obj for obj in C.selected_objects[:] if obj != active_obj]
    for obj in sel_objs:
        for c in obj.constraints[:]:
            if c.type == "CHILD_OF":
                obj.constraints.remove(c)

        const = obj.constraints.new(type="CHILD_OF")
        const.target = active_obj


class OBJECT_OT_make_child_of(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "object.make_child_of"
    bl_label = "Make Child Of"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and len(context.selected_objects) > 1

    def execute(self, context):
        main(context)
        return {"FINISHED"}
