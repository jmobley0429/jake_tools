import bpy


def get_objects(context):
    objs_to_parent = set()
    armature = None
    for obj in context.selected_objects:
        if obj.type == "MESH":
            objs_to_parent.add(obj)
        elif obj.type == "ARMATURE" and armature is None:
            armature = obj
    return armature, objs_to_parent


def clear_vertex_groups(obj):
    groups = obj.vertex_groups[:]
    while groups:
        obj.vertex_groups.remove(groups.pop())


def get_vertex_group(obj, v_group_name):
    try:
        vg = obj.vertex_groups[v_group_name]
    except KeyError:
        clear_vertex_groups(obj)
        vg = obj.vertex_groups.new(name=v_group_name)
    return vg


def get_armature_modifier(armature, obj):
    for mod in obj.modifiers:
        if mod.type == "ARMATURE":
            print(mod.type, mod.object, mod.object == armature)
            if mod.object == armature:
                print("USING EXISTING")
                arm_mod = mod
    else:
        arm_mod = obj.modifiers.new(name="Armature", type="ARMATURE")
        arm_mod.object = armature
        print("USING NEW")
    return arm_mod


def main(context):
    C = context
    active_bone = C.active_pose_bone
    v_group_name = active_bone.name
    armature, objs = get_objects(C)

    for obj in objs:
        get_armature_modifier(armature, obj)
        vg = get_vertex_group(obj, v_group_name)
        verts = [v.index for v in obj.data.vertices]
        vg.add(verts, 1.0, "REPLACE")


def poll_op(context):
    if context.mode != "POSE":
        return False
    if context.active_pose_bone is None:
        return False
    if "ARMATURE" not in {obj.type for obj in context.selected_objects}:
        return False
    if len(context.selected_objects) < 2:
        return False
    return True


class RIG_OT_quick_parent_object_to_bone(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "pose.quick_parent_object_to_bone"
    bl_label = "Quick Parent Object to Bone"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return poll_op(context)

    def execute(self, context):
        main(context)
        return {"FINISHED"}
