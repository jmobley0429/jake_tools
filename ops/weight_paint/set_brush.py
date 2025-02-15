import bpy


BRUSH_TYPES = "Draw Average Blur Smear gradient sample_weight".split()
BRUSH_IDS = [f"builtin_brush.{brush}" for brush in BRUSH_TYPES]
DRAW_BRUSH_TYPES = [
    "Add",
    "Subtract",
    "Darken",
    "Multiply",
    "Lighten",
    "Draw",
]


def get_brush_enum_items():
    ids = BRUSH_TYPES
    names = descriptions = [id.replace("_", " ").capitalize() for id in BRUSH_TYPES]
    return [tuple([id, name, desc]) for id, name, desc in zip(ids, names, descriptions)]


def get_draw_brush_enum_items():
    names = ids = descriptions = DRAW_BRUSH_TYPES
    return [tuple([id, name, desc]) for id, name, desc in zip(ids, names, descriptions)]


def get_brushes():
    return {brush.name: brush for brush in bpy.data.brushes[:] if brush.name in DRAW_BRUSH_TYPES}


def set_brush(context, **args):
    args = args.copy()
    brush_type = args.pop('brush_type')
    draw_brush_type = args.pop('draw_brush_type')

    

    if brush_type in "gradient sample_weight".split():
        id_prefix = "builtin."
    else:
        id_prefix = "builtin_brush."
    brush_id = f"{id_prefix}{brush_type}"

    bpy.ops.wm.tool_set_by_id(name=brush_id)
    if brush_type == "Draw":
        ts_modes = {
            "PAINT_WEIGHT": "weight_paint", 
            "PAINT_VERTEX": "vertex_paint"
        }
        mode_attr = ts_modes[context.mode]
        tool_settings = getattr(context.tool_settings, mode_attr)
        draw_brush = get_brushes()[draw_brush_type]
        setattr(tool_settings, "brush", draw_brush)
        # context.tool_settings.weight_paint.brush = 


BRUSH_MODES = [
    "PAINT_WEIGHT",
    "PAINT_VERTEX"
]


class PAINT_OT_set_brush(bpy.types.Operator):
    bl_idname = "brush.set_brush"
    bl_label = "Set Brush"
    bl_options = {'REGISTER', 'UNDO'}

    brush_type: bpy.props.EnumProperty(
        items=get_brush_enum_items(),
        name='Brush Type',
        description='Brush Type',
    )

    draw_brush_type: bpy.props.EnumProperty(
        items=get_draw_brush_enum_items(),
        name='Draw Brush Type',
        description='Draw Brush Type',
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.mode in BRUSH_MODES

    def execute(self, context):
        args = self.as_keywords()
        set_brush(context, **args)
        return {"FINISHED"}



