import bpy


def main(context):
    C = context
    for obj in C.selected_objects[:]:
        es = obj.modifiers.new(type="EDGE_SPLIT", name="EdgeSplit")
        es.split_angle = 0
        es.use_edge_sharp = 0
        sm = obj.modifiers.new(type="SMOOTH", name="Smooth")
        sm.factor = 0.01


class OBJECT_OT_add_collision_modifiers(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "object.add_collision_modifiers"
    bl_label = "Add Collision Modifiers"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {"FINISHED"}
