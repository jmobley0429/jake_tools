from bpy.types import Menu


class IMAGE_MT_uvs_snap_pie_custom(Menu):
    bl_label = "Snap"
    bl_idname = "IMAGE_MT_uvs_snap_pie_custom"

    def draw(self, _context):
        import string

        layout = self.layout
        pie = layout.menu_pie()

        layout.operator_context = "EXEC_REGION_WIN"

        pie.operator(
            "uv.snap_selected",
            text="Selected to Pixels",
            icon="RESTRICT_SELECT_OFF",
        ).target = "PIXELS"
        pie.operator(
            "uv.snap_cursor",
            text="Cursor to Pixels",
            icon="PIVOT_CURSOR",
        ).target = "PIXELS"
        pie.operator(
            "uv.snap_cursor",
            text="Cursor to Selected",
            icon="PIVOT_CURSOR",
        ).target = "SELECTED"
        col = pie.column()
        col.label(text="Snap to Midpoint")
        for ax in list("xy"):
            spl = col.split()
            for side in "MIN MAX".split():
                label = f"{ax.capitalize()} - {string.capwords(side)}"
                op = spl.operator("uv.snap_uvs_to_midpoint", text=label)
                op.direction = ax
                op.bounds = side
        pie.operator(
            "uv.snap_selected",
            text="Selected to Cursor",
            icon="RESTRICT_SELECT_OFF",
        ).target = "CURSOR"
        pie.operator(
            "uv.snap_selected",
            text="Selected to Cursor (Offset)",
            icon="RESTRICT_SELECT_OFF",
        ).target = "CURSOR_OFFSET"
        pie.operator(
            "uv.snap_selected",
            text="Selected to Adjacent Unselected",
            icon="RESTRICT_SELECT_OFF",
        ).target = "ADJACENT_UNSELECTED"
        pie.operator(
            "uv.snap_cursor",
            text="Cursor to Origin",
            icon="PIVOT_CURSOR",
        ).target = "ORIGIN"


kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "UV Editor",
        "letter": "S",
        "shift": 1,
        "ctrl": 0,
        "alt": 0,
        "space_type": "IMAGE_EDITOR",
        "region_type": "WINDOW",
        "keywords": {"name": IMAGE_MT_uvs_snap_pie_custom.bl_idname},
    }
]
