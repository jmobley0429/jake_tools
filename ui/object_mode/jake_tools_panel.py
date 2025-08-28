import bpy
from bpy.types import Menu
from jake_tools.ops.mesh.cleanup_mesh import (
    MESH_OT_cleanup_center_edge_verts,
    MESH_OT_cleanup_handle_ngons,
    MESH_OT_cleanup_select_short_edges,
    MESH_OT_cleanup_select_small_faces,
)

from jake_tools.ops.modifier.triangulate_modifier_add import (
    OBJECT_OT_triangulate_modifier_add,
)
from jake_tools.ops.object_mode.vertex_color_tools import (
    OBJECT_OT_CopyVcolFromActive,
    OBJECT_OT_generate_random_v_colors_per_obj,
)
from jake_tools.ops.render.rebake_eevee_scene import RENDER_OT_BakeEeveeScene


def jake_tools_panel(context, layout):
    mpm_props = context.scene.mpm_props
    col = layout.column(align=True)
    box = col.box()
    box.label(text="Texturing Tools")
    col = box.column(align=True)
    col.label(text="Assign Random VCol")
    row = col.row(align=True)
    op = row.operator(
        OBJECT_OT_generate_random_v_colors_per_obj.bl_idname, text="Single Random"
    )
    op.multi_obj = False
    op = row.operator(
        OBJECT_OT_generate_random_v_colors_per_obj.bl_idname, text="Multi Object"
    )
    op.multi_obj = True
    row = col.row(align=True)
    row.prop(
        mpm_props,
        "custom_vertex_color",
    )
    row = col.row(align=True)
    op = row.operator(
        OBJECT_OT_generate_random_v_colors_per_obj.bl_idname,
        text="Set Single Color",
    )
    op.color_picker = True
    row = col.row(align=True)
    row.operator_context = "EXEC_DEFAULT"
    op = row.operator(
        OBJECT_OT_CopyVcolFromActive.bl_idname, text="Copy VCol from Active"
    )
    col = layout.column(align=True)
    box = col.box()
    box.label(text="Mesh Cleanup Tools")
    col = box.column(align=True)
    row = col.row()
    row.operator(MESH_OT_cleanup_select_short_edges.bl_idname)
    row = col.row()
    row.operator(MESH_OT_cleanup_select_small_faces.bl_idname)
    row = col.row()
    row.operator(MESH_OT_cleanup_select_short_edges.bl_idname)
    row = col.row()
    row.operator(MESH_OT_cleanup_handle_ngons.bl_idname)
    row = col.row()
    row.operator(MESH_OT_cleanup_center_edge_verts.bl_idname)

    col = layout.column(align=True)
    box = col.box()
    box.label(text="Prop Tools")
    col = box.column(align=True)
    row = col.row()
    row.operator(OBJECT_OT_triangulate_modifier_add.bl_idname)

    box.label(text="Render Tools")
    col = box.column(align=True)
    row = col.row()
    row.operator(RENDER_OT_BakeEeveeScene.bl_idname)


class OBJECT_PT_jake_tools_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Jake Tools"
    bl_label = "Jake Tools"
    bl_idname = "OBJECT_PT_jake_tools_panel"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        jake_tools_panel(context, self.layout)


kms = []
