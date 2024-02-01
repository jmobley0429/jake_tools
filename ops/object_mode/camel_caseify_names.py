import bpy
import re


def format_str(string):
    if string[0].isdigit():
        return "_" + string
    elif string.isupper():
        return string
    return string.capitalize()


def get_new_name(obj, add_sm=True):
    name_strs = [format_str(st) for st in obj.name.split("_") if st != "SM"]
    cc_name = "".join(name_strs)
    if add_sm:
        cc_name = f"SM_{cc_name}"
    return cc_name


def main(context, args):
    add_sm = args.pop("add_sm_prefix")
    for obj in context.selected_objects:
        obj.name = get_new_name(obj, add_sm=add_sm)


class OBJECT_OT_camel_caseify_names(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "object.camel_caseify_names"
    bl_label = "Camel Caseify Names"
    bl_description = "Camel Caseify Names, CTRL > disable adding SM prefix."
    bl_options = {"REGISTER", "UNDO"}

    add_sm_prefix: bpy.props.BoolProperty(name="Add SM Prefix", default=True)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and len(context.selected_objects) > 0

    def invoke(self, context, event):
        if event.ctrl:
            self.add_sm_prefix = False
        return self.execute(context)

    def execute(self, context):
        main(context, self.as_keywords())
        return {"FINISHED"}
