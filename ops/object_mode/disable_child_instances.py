import bpy
import utils


def get_active_coll(context):
    active_coll = context.collection
    obj = context.active_object
    ao_coll = obj.users_collection[0]
    if ao_coll != active_coll:
        active_coll = ao_coll
    return active_coll


def get_instance_mod(obj):
    for mod in obj.modifiers:
        if mod.type == "NODES" and mod.node_group is not None:
            if "Instance" in mod.node_group.name:
                return mod


def main(context):
    objs = bpy.data.objects
    active_coll = get_active_coll(context)

    statuses = []

    for obj in objs:
        if obj.type in {"MESH", "CURVE"}:
            mod = get_instance_mod(obj)
            if mod:
                input_id = utils.get_node_group_input_id(mod, "Collection")
                mod_coll = mod[input_id]
                if mod_coll == active_coll:
                    status = mod.show_viewport
                    mod.show_viewport = not status
                    statuses.append(not status)
    return statuses


def get_status_msg(shown_statuses):
    num_statuses = len(shown_statuses)
    plural = "s" if num_statuses > 1 else ""
    msg = f"{num_statuses} Reference Object{plural} set to: "
    hidden_msg = "Visible" if all(shown_statuses) else "Hidden"
    print(msg, hidden_msg)
    msg = msg + hidden_msg
    if num_statuses < 1:
        msg = "No collection references found!"
    return msg


class OBJECT_OT_disable_child_instances(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "object.disable_child_instances"
    bl_label = "Disable Child GN Instances"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        shown_statuses = main(context)
        msg = get_status_msg(shown_statuses)
        self.report({"INFO"}, msg)
        return {"FINISHED"}
