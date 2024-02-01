import bpy
from bpy.types import Menu


class PIE_MT_PhysicsSubPie(Menu):
    bl_idname = "PIE_MT_PhysicsSubPie"
    bl_label = "Pie Add Physics Modifiers"

    @classmethod
    def poll(cls, context):
        ob = context.object
        return ob and ob.type != "GPENCIL"

    def draw(self, context):
        layout = self.layout
        op = layout.operator(
            "object.multiple_modifiers_add", text="Cloth", icon="MOD_CLOTH"
        )
        op.mod_type = "CLOTH"
        op = layout.operator(
            "object.multiple_modifiers_add", text="Collision", icon="MOD_PHYSICS"
        )
        op.mod_type = "COLLISION"
        op = layout.operator(
            "object.multiple_modifiers_add", text="Particle", icon="PARTICLES"
        )
        op.mod_type = "PARTICLE_SYSTEM"
        op = layout.operator(
            "object.multiple_modifiers_add", text="Soft Body", icon="MOD_SOFT"
        )
        op.mod_type = "SOFT_BODY"
        op = layout.operator(
            "rigidbody.object_add", text="Rigid Body", icon="RIGID_BODY"
        )
