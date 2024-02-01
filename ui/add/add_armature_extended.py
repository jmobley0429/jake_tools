from bpy.types import Menu


class PIE_MT_add_armature_extended(Menu):
    bl_idname = "PIE_MT_add_armature_extended"
    bl_label = "Pie Add Armature Extended"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.armature_add", text="Single Bone", icon="BONE_DATA")
        layout.menu("ARMATURE_MT_Basic_class")
        layout.menu("ARMATURE_MT_Animals_class")
