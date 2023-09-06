import bpy
from custom_operator import *
import numpy as np

def set_vertex_color(vertex_color, mesh, color_layer, ):
    i = 0
    for poly in mesh.polygons[:]:
        for loop in poly.loop_indices:
            color_layer.data[i].color = vertex_color
            i += 1

def get_masked_channels(args):
    masked_channels = []
    for name, value in args.items():
        if 'channel' in name:
            masked_channels.append(float(value))
    masked_channels.append(1.0)
    return np.array(masked_channels)

        

def generate_random_v_colors_per_obj(context, **args):
    multi_obj = args.pop("multi_obj")
    color_picker = args.pop("color_picker")
    objs = context.selected_objects[:]
    

    colors = []
    margin = 0.03
    channel_mask = get_masked_channels(args)

    def generate_color():
        too_close = False
        color = np.random.random_sample((3,))
        color = np.append(color, 1.0)
        for col in colors:
            col_avg = np.mean(col)
            new_col_avg = np.mean(color)
            diff = col_avg - new_col_avg
            if abs(diff) < margin:
                too_close = True
        if not too_close:
            colors.append(color)
            return color
        return generate_color()

    if color_picker:
        color = context.scene.mpm_props.custom_vertex_color
    elif not multi_obj:
        color = generate_color()

    for obj in objs:
        if obj.type == "MESH":
            mesh = obj.data
            vcol_layer = get_mesh_vcol_layer(mesh)
            if multi_obj:
                color = generate_color()
            color *= channel_mask
            set_vertex_color(color, mesh, vcol_layer)

class OBJECT_OT_generate_random_v_colors_per_obj(bpy.types.Operator):
    bl_idname = "object.generate_random_v_colors_per_obj"
    bl_label = "Random Vertex Color Per Object"
    bl_options = {"REGISTER", "UNDO"}

    multi_obj: bpy.props.BoolProperty(
        default=False,
        name="Multi Object",
        description="multi_obj: True, Give each selected object it's own random color. False: Set all objects to one color",
    )
    color_picker: bpy.props.BoolProperty(
        default=False,
        name="Color Picker",
        description="If true, use color picker to assign vertex_color.",
    )

    red_channel: bpy.props.BoolProperty(
        default=True,
        name="R",
    )
    green_channel: bpy.props.BoolProperty(
        default=True,
        name="G",
    )
    blue_channel: bpy.props.BoolProperty(
        default=True,
        name="B",
    )

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT" and context.selected_objects

    def execute(self, context):
        args = self.as_keywords()
        generate_random_v_colors_per_obj(context, **args)
        return {"FINISHED"}
    
def get_mesh_vcol_layer(mesh):
    try:
       color_layer = mesh.vertex_colors["Col"]
    except KeyError:
       color_layer = mesh.vertex_colors.new()
    return color_layer


def get_active_obj_vcol(obj):
    mesh = obj.data
    color_layer = get_mesh_vcol_layer(mesh)
    rgb_values = []
    i = 0
    for poly in mesh.polygons[:]:
        for loop in poly.loop_indices:
            rgb_val = color_layer.data[i].color[:]
            rgb_values.append(np.array(rgb_val))
            i += 1

    return np.mean(rgb_values, axis=0)


def copy_vcol_from_active(context):
    objs = context.selected_objects
    active_obj = context.active_object
    active_vcol = get_active_obj_vcol(active_obj)
    for obj in objs:
        if obj.type == "MESH" and obj != active_obj:
            mesh = obj.data
            color_layer = get_mesh_vcol_layer(mesh)
            set_vertex_color(active_vcol, mesh, color_layer)




class OBJECT_OT_CopyVcolFromActive(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "object.copy_vcol_from_active"
    bl_label = "Copy Vertex Color from Active"

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None and len(context.selected_objects[:]) > 1
        )

    def execute(self, context):
        copy_vcol_from_active(context)
        return {"FINISHED"}


def copy_obj_name(context):
    for obj in bpy.context.selected_objects[:]:
        active_obj = bpy.context.view_layer.objects.active
        if obj != active_obj:
            obj.name = active_obj.name