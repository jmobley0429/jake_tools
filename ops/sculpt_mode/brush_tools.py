import bpy
from pathlib import Path
from jake_tools.ops.custom_operator import CustomModalOperator

ROOT = Path(__file__).parent.parent.resolve()
custom_shape_fp = ROOT.joinpath("resources", "gizmo_circle_mesh.json")


class Brush:
    def __init__(self, context):
        self.context = context
        self.mode = context.mode
        self.ts = context.tool_settings

        BRUSH_ATTRIBUTES = {
            "SCULPT": {
                "brush": self.ts.sculpt.brush,
                "settings": self.ts.sculpt.brush,
                "ss_attr": "use_smooth_stroke",
                "ss_radius_attr": "smooth_stroke_radius",
            },
            "PAINT_GPENCIL": {
                "brush": self.ts.gpencil_paint.brush,
                "settings": self.ts.gpencil_paint.brush.gpencil_settings,
                "ss_attr": "use_settings_stabilizer",
                "ss_radius": "use_settings_stabilizer",
            },
        }
        self.brush_attrs = BRUSH_ATTRIBUTES[self.mode]

    @property
    def brush(self):
        return self.brush_attrs["brush"]

    @property
    def settings(self):
        return self.brush_attrs["settings"]

    @property
    def ss_attr(self):
        return self.brush_attrs["ss_attr"]

    @property
    def use_smooth_stroke(self):
        attr = self.brush_attrs["ss_attr"]
        return getattr(self.settings, attr)


class BRUSH_OT_toggle_stabilize_stroke(bpy.types.Operator):

    bl_idname = "brush.toggle_stabilize_stroke"
    bl_label = "Toggle Stabilize Stroke"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode in {"SCULPT", "PAINT_GPENCIL"}

    def execute(self, context):
        br = Brush(context)
        settings = br.brush
        attr = br.ss_attr
        setattr(settings, attr, not br.use_smooth_stroke)
        return {"FINISHED"}


class BRUSH_OT_adjust_stabilize_radius(CustomModalOperator, bpy.types.Operator):

    bl_idname = "brush.adjust_stabilize_radius"
    bl_label = "Adjust Stabilize Stroke Radius"
    bl_options = {"REGISTER", "UNDO"}

    radius: bpy.props.FloatProperty(name="Smooth Stroke Radius")

    @classmethod
    def poll(cls, context):
        mode = context.mode in {"SCULPT", "PAINT_GPENCIL"}
        if not mode:
            return False
        cls.br = Brush(context)
        use_ss = cls.br.use_smooth_stroke
        return all([mode, use_ss])

    def invoke(self, context, event):
        self.brush = self.br.brush
        self.radius = self.brush.smooth_stroke_radius
        self.init_mouse_x = event.mouse_x

        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        msg = f"SMOOTH STROKE RADIUS: {self.radius:.2f}"
        self.display_modal_info(msg, context)
        modifier = 0.1
        delta = 0
        if event.shift:
            modifier = 0.01
        if event.type == "MOUSEMOVE":
            delta = self.init_mouse_x - event.mouse_x
            delta *= modifier
            self.init_mouse_x = event.mouse_x
        elif event.type in {"RIGHTMOUSE", "ESC"}:
            return self.exit_modal(context, cancelled=True)
        elif event.type == "LEFTMOUSE":
            self.brush.smooth_stroke_radius = int(self.radius)
            return self.exit_modal(context)
        print(delta)
        self.radius -= delta
        return {"RUNNING_MODAL"}


kms = [
    {
        "keymap_operator": BRUSH_OT_toggle_stabilize_stroke.bl_idname,
        "name": "Sculpt",
        "letter": "S",
        "shift": 1,
        "ctrl": 0,
        "alt": 1,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {},
    },
    {
        "keymap_operator": BRUSH_OT_adjust_stabilize_radius.bl_idname,
        "name": "Sculpt",
        "letter": "F",
        "shift": 1,
        "ctrl": 0,
        "alt": 1,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {},
    },
]
