# modifier
import bpy
from bpy.types import Operator


class OBJECT_OT_custom_rigid_body_add(Operator):
    bl_idname = "object.custom_rigid_body_add"
    bl_label = "Rigid Body"
    bl_description = "Adds Rigid Body to all selected objects. ALT > Adds as Passive."
    bl_options = {"REGISTER", "UNDO"}

    set_as_passive: bpy.props.BoolProperty(
        name="Passive", default=False, options={"SKIP_SAVE"}
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def invoke(self, context, event):
        if event.alt:
            self.set_as_passive = True
        return self.execute(context)

    def execute(self, context):
        bpy.ops.rigidbody.object_add()
        if self.set_as_passive:
            context.active_object.rigid_body.type = "PASSIVE"
        bpy.ops.rigidbody.object_settings_copy()

        return {"FINISHED"}
