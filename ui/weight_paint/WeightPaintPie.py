from bpy.types import Menu


class PIE_MT_PaintBrushPie(Menu):
    bl_idname = "PIE_MT_PaintBrushPie"
    bl_label = "Switch Paint Brush Pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        op = pie.operator("brush.set_brush", text="Add")
        op.brush_type = "Draw"
        op.draw_brush_type = "Add"

        op = pie.operator("brush.set_brush", text="Subtract")
        op.brush_type = "Draw"
        op.draw_brush_type = "Subtract"
        box = pie.box()
        box.label(text="Draw Brushes")
        col = box.column()
        op = col.operator(
            "brush.set_brush",
            text="Multiply",
        )
        op.brush_type = "Draw"
        op.draw_brush_type = "Multiply"

        op = col.operator("brush.set_brush", text="Darken")
        op.brush_type = "Draw"
        op.draw_brush_type = "Darken"

        op = col.operator("brush.set_brush", text="Lighten")
        op.brush_type = "Draw"
        op.draw_brush_type = "Lighten"

        op = pie.operator("brush.set_brush", text="Smear")
        op.brush_type = "Smear"

        op = pie.operator("brush.set_brush", text="Average")
        op.brush_type = "Average"
        if context.mode == "PAINT_WEIGHT":
            op = pie.operator("brush.set_brush", text="Gradient")
            op.brush_type = "gradient"

        op = pie.operator("brush.set_brush", text="Blur")
        op.brush_type = "Blur"


kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Weight Paint",
        "letter": "W",
        "shift": 1,
        "ctrl": 0,
        "alt": 0,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": "PIE_MT_PaintBrushPie"},
    },
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Vertex Paint",
        "letter": "W",
        "shift": 1,
        "ctrl": 0,
        "alt": 0,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": "PIE_MT_PaintBrushPie"},
    },
]
