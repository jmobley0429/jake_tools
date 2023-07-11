import bpy


class OBJECT_OT_clean_up_quadremesh_names(bpy.types.Operator):
    bl_idname = "object.clean_up_quadremesh_names"
    bl_label = "Clean Up QuadRemesh Names"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        for obj in bpy.data.objects[:]:
            obj.name = obj.name.replace("Retopo_", "")
        return {"FINISHED"}
