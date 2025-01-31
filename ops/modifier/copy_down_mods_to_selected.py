import bpy


def get_properties(src_mod):
    return [
        prop.identifier for prop in src_mod.bl_rna.properties if not prop.is_readonly
    ]


def get_active_mod_index(obj):
    mods = obj.modifiers
    active_mod = mods.active
    active_index = mods[:].index(active_mod)
    return active_index


def copy_modifier(mod, obj):
    copied = obj.modifiers.new(mod.name, mod.type)
    props = get_properties(mod)
    for prop in props:
        value = getattr(mod, prop)
        setattr(copied, prop, value)


def main(context):
    sel_objs = set(context.selected_objects)

    ao = context.active_object
    sel_objs = sel_objs - set([ao])
    ao_mods = ao.modifiers
    active_mod_index = get_active_mod_index(ao)

    for obj in sel_objs:
        if obj.type in {"MESH", "CURVE"} and obj is not ao:
            for mod in ao.modifiers[active_mod_index + 1 :]:
                copy_modifier(mod, obj)


class MODIFIER_OT_copy_down_mods_to_selected(bpy.types.Operator):
    """Copies all modifiers below the currently active modifier on the active object to each other selected object"""

    bl_idname = "object.copy_down_mods_to_selected"
    bl_label = "Copy Lower Mods To Selected"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and len(context.selected_objects) > 1

    def execute(self, context):
        main(context)
        return {"FINISHED"}
