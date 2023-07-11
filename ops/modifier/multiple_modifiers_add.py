import bpy
from custom_operator import *

class OBJECT_OT_AddMultipleModifiers(bpy.types.Operator):
    bl_idname = 'object.multiple_modifiers_add'
    bl_label = 'Add Multiple Modifiers'
    bl_options = {'REGISTER', "UNDO"}

    mod_type: bpy.props.StringProperty()
    is_custom_mod: bpy.props.BoolProperty(default=False)

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) >= 1 and context.active_object
    
    def execute(self, context):
        
        for obj in context.selected_objects[:]:
            if obj.type in {"MESH", "CURVE"}:
                mod_name = self.mod_type.replace('_', ' ').capitalize()
                mod = obj.modifiers.new(name=mod_name, type=self.mod_type)

        return {"FINISHED"}
    
