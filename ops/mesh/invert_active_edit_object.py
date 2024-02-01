import bpy


class MESH_OT_invert_active_edit_object(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "mesh.invert_active_edit_object"
    bl_label = "Invert Active Edit Object"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) == 2

    def execute(self, context):
        ao = context.view_layer.objects.active
        ao_set = set([context.view_layer.objects.active])
        objs = set(context.selected_objects[:]) - ao_set
        new_ao = objs.pop()
        bpy.ops.object.mode_set(mode="OBJECT")
        ao.select_set(False)
        context.view_layer.objects.active = new_ao
        bpy.ops.object.mode_set(mode="EDIT")

        return {"FINISHED"}
