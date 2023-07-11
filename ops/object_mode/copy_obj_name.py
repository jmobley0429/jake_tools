import bpy


def copy_obj_name(context):
    for obj in context.selected_objects[:]:
        active_obj = context.view_layer.objects.active
        if obj != active_obj:
            obj.name = active_obj.name


class OBJECT_OT_CopyObjName(bpy.types.Operator):
    bl_idname = "object.copy_obj_name"
    bl_label = "Copy Object Name"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        copy_obj_name(context)
        return {"FINISHED"}
