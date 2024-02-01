from bpy.types import Menu


class PIE_MT_MeshSubPie(Menu):
    bl_idname = "PIE_MT_MeshSubPie"
    bl_label = "Pie Add Mesh Modifiers"

    @classmethod
    def poll(cls, context):
        ob = context.object
        return ob and ob.type != "GPENCIL"

    def draw(self, context):
        layout = self.layout
        op = layout.operator(
            "object.multiple_modifiers_add", text="Multires", icon="MOD_MULTIRES"
        )
        op.mod_type = "MULTIRES"
        layout.operator("object.custom_remesh", text="Remesh", icon="MOD_REMESH")
        layout.operator("object.custom_decimate", text="Decimate", icon="MOD_DECIM")
        op = layout.operator(
            "object.multiple_modifiers_add", text="Smooth", icon="MOD_SMOOTH"
        )
        op.mod_type = "SMOOTH"
        op = layout.operator(
            "modifier.weld_modifier_modal", text="Weld", icon="AUTOMERGE_OFF"
        )

        op = layout.operator(
            "object.triangulate_modifier_add", text="Triangulate", icon="TRIA_UP"
        )
