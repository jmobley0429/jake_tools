#modifier
from bpy.types import Operator

class OBJECT_OT_triangulate_modifier_add(Operator):
    bl_idname = "object.triangulate_modifier_add"
    bl_label = "Triangulate"
    bl_description = "Adds Triangulate Modifier to all selected objects."
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        for obj in context.selected_objects:
            mods = [mod.type for mod in obj.modifiers[:]]
            if obj.type == "MESH" and "TRIANGULATE" not in mods:
                mod = obj.modifiers.new("Triangulate", "TRIANGULATE")
                mod.keep_custom_normals = True
        return {"FINISHED"}