import bpy
from bpy.types import Operator

def get_mod_attrs(mod):
    return [(attr, getattr(mod, attr)) for attr in dir(mod)]


def apply_then_reapply_modifier(obj):
    mods = []
    for mod in obj.modifiers[:]:
        mod_data = {}    
        mod_data['type'] = mod.type
        mod_data['name'] = mod.name
        mod_data['attrs'] = get_mod_attrs(mod)
        mods.append(mod_data)
        bpy.ops.object.modifier_apply(modifier=mod.name)
    for mod in mods:
        remod = obj.modifiers.new(mod['name'], mod['type'])
        for attr, val in mod['attrs']:
            try:
                setattr(remod, attr, val)
            except AttributeError:
                continue
            

class OBJECT_OT_apply_then_readd_modifiers(Operator):
    """Convert object to another object type. CTRL > Keep Original"""

    bl_idname = "object.apply_then_readd_modifiers"
    bl_label = "Apply Then Reapply Mods"
    bl_description = """Applies all modifiers, then re-adds them in the same state as before"""
    bl_options = {"REGISTER", "UNDO"}


    @classmethod
    def poll(cls, context):
        return context.view_layer.objects.active is not None and "OBJECT" in context.mode


    def execute(self, context):
        obj = context.view_layer.objects.active
        apply_then_reapply_modifier(obj)
        return {"FINISHED"}
