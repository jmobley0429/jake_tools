from bpy.types import Menu


class PIE_MT_NormalSubPie(Menu):
    bl_idname = "PIE_MT_NormalSubPie"
    bl_label = "Pie Add Normal Modifiers"

    @classmethod
    def poll(cls, context):
        ob = context.object
        return ob and ob.type != "GPENCIL"

    def draw(self, context):
        layout = self.layout
        op = layout.operator(
            "object.modifier_add_node_group", text="AutoSmooth", icon="SHADING_RENDERED"
        )
        op.asset_library_type = "ESSENTIALS"
        op.asset_library_identifier = ""
        op.relative_asset_identifier = (
            "geometry_nodes\\smooth_by_angle.blend\\NodeTree\\Smooth by Angle"
        )
        op = layout.operator(
            "object.custom_weighted_normal",
            text="Weighted Normal",
            icon="NORMALS_VERTEX",
        )
        op = layout.operator(
            "object.multiple_modifiers_add", text="UV Project", icon="MOD_UVPROJECT"
        )
        op.mod_type = "UV_PROJECT"
        op = layout.operator(
            "object.custom_dt_modifier_add", text="Data Transfer", icon="CON_TRANSLIKE"
        )
