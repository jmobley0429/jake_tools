from bpy.types import Menu

class PIE_MT_UVUnwrapPie(Menu):
    bl_idname = "PIE_MT_UVUnwrapPie"
    bl_label = "UV Unwrap Pie"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        layout = self.layout
        props = context.scene.uvp2_props
        pie = layout.menu_pie()
        # L
        col = pie.column()
        row = col.row()
        row.prop(props, "heuristic_enable")
        row = col.row()
        row.operator("uvpackmaster2.uv_pack", text="Pack")
        row = col.row()
        row.prop(props, "heuristic_search_time")
        # R
        pie.operator("uv.textools_rectify")
        # B
        pie.operator('uv.seams_from_islands', text="Island Seams")
        # T
        pie.operator('uv.toggle_uv_sync_selection')
        col = pie.column()
        col.label(text="Unwrap")
        col.scale_x = 0.9
        spl = col.split()
        spl.operator("uv.pin", text="Pin")
        spl.operator("uv.pin", text="Unpin").clear = True
        spl = col.split(factor=0.5, align=True)
        spl.operator("uv.unwrap", text="Unwrap")
        row = spl.row(align=True)
        row.operator("uv.textools_uv_unwrap", text="U").axis = "x"
        row.operator("uv.textools_uv_unwrap", text="V").axis = "y"

        col = pie.column()
        col.label(text="Add to Lock Groups")
        col.scale_x = 1
        spl = col.split()
        spl.operator("uvpackmaster2.set_free_island_lock_group",
                     text="Current")
        spl.operator("uvpackmaster2.set_island_lock_group", text="Free")
        spl = col.split()
        spl.prop(props, "lock_groups_enable", text="Enable")
        col = pie.column()
        col.scale_x = 0.8
        spl = col.split()
        col.label(text="Pixel Spacing")
        row = col.row(align=True)
        row.prop(props, "pixel_margin", text="Margin")
        row = col.row(align=True)
        row.prop(props, "pixel_padding", text="Padding")
        row = col.row(align=True)
        row.prop(props, "pixel_margin_tex_size", text="Tex. Size")
        col = pie.column()
        col.scale_x = 0.9
        spl = col.split()
        col.label(text="Transform")
        spl = col.split()
        spl.operator("uv.textools_uv_crop")
        spl.operator("uv.textools_uv_fill")
        spl = col.split()
        spl.operator("uv.textools_island_align_edge", text="Align Edge")
        spl.operator("uv.textools_island_align_world", text="Align World")

kms = [
        {
        "keymap_operator": "wm.call_menu_pie",
        "name": "UV Editor",
        "letter": "Q",
        "shift": 1,
        "ctrl": 1,
        "alt": 0,
        "space_type": "IMAGE_EDITOR",
        "region_type": "WINDOW",
        "keywords": {"name": PIE_MT_UVUnwrapPie.bl_idname},
    },
]