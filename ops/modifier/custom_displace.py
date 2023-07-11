# modifier

import bpy
import utils
from mathutils import Vector
import numpy as np
import re
from bpy.types import Operator
from custom_operator import *




# initialize values at beginning of modal, mouse pos, object location, rot scale


# add empty object 


# add displace modifier


# initialize textures


# create collection for organizing coord objects


class DisplaceTextureObjects:
    
    texture_types = ["Clouds", "Musgrave", "Voronoi", "Wood"]

    def __init__(self):
        self.texture_objects = []
        self.current_index = 0

    def initialize_texture_objects(self):
        for texture_type in self.texture_types:
            texture_name = f"Displace_{texture_type}"
            texture_object = bpy.data.textures.new(texture_name, texture_type.upper())
            self.texture_objects.append(texture_object)
    @property
    def current_texture(self):
        return self.texture_objects[self.current_index]
    
    def change_current_texture(self, forward=True):
        next_index = 1 if forward else -1
        self.current_index = (self.current_index + next_index) % len(self.texture_types)

    def cleanup_textures(self, cancelled=False):
        for texture in self.texture_objects[:]:
            if cancelled:
                bpy.data.textures.remove(texture)
            else:
                if texture != self.current_texture:
                    bpy.data.textures_remove(texture)

    
class DisplaceCoordinateObject:

    def __init__(self, context):
        self.context = context 
        self.active_object = context.active_object

    def initialize_mouse_values(self, event):
        self.init_x = event.mouse_x
        self.init_y = event.mouse_y
    
    def initialize_empty_object(self):
        empty_name = f"{self.active_object.name}_DisplaceCoord"
        self.coord_object = bpy.data.objects.new(empty_name, object_data=None)
        self.dc_collection = utils.get_or_create_collection("DisplaceCoords")
        self.dc_collection.objects.link(self.coord_object)
        self.coord_object.location = self.active_object.location

        

        



    







class Displacer(OperatorBaseClass, CustomModalOperator,):
    textures = ["Clouds", "Musgrave", "Voronoi", "Wood"]
    
    texture_properties = {
        "MUSGRAVE": {
            "basis": "noise_basis",
            "type": "musgrave_type",
            "basis_list": [
                "BLENDER_ORIGINAL",
                "VORONOI_F1",
                "VORONOI_F2_F1",
                "VORONOI_F2",
                "VORONOI_F3",
                "VORONOI_F4",
                "ORIGINAL_PERLIN",
                "VORONOI_CRACKLE",
                "IMPROVED_PERLIN",
                "CELL_NOISE",
            ],
            "type_list": [
                "HETERO_TERRAIN",
                "FBM",
                "HYBRID_MULTIFRACTAL",
                "RIDGED_MULTIFRACTAL",
                "MULTIFRACTAL",
            ],
            "mod_channel": {
                "D": "dimension_max",
                "L": "lacunarity",
                "O": "octaves",
                "I": "noise_intensity",
                "B": "intensity",
                "C": "contrast",
                "S": "noise_scale",
            },
            "default_vals": {},
        },
        "CLOUDS": {
            "basis": "noise_basis",
            "type": "noise_type",
            "basis_list": [
                "BLENDER_ORIGINAL",
                "VORONOI_F1",
                "VORONOI_F2_F1",
                "VORONOI_F2",
                "VORONOI_F3",
                "VORONOI_F4",
                "ORIGINAL_PERLIN",
                "VORONOI_CRACKLE",
                "IMPROVED_PERLIN",
                "CELL_NOISE",
            ],
            "type_list": ["SOFT_NOISE", "HARD_NOISE"],
            "mod_channel": {
                "B": "intensity",
                "C": "contrast",
                "S": "noise_scale",
            },
            "default_vals": {},
        },
        "VORONOI": {
            "basis": "distance_metric",
            "type": "color_mode",
            "basis_list": [
                "DISTANCE",
                "MANHATTAN",
                "CHEBYCHEV",
                "MINKOWSKI",
            ],
            "type_list": [
                "POSITION",
                "POSITION_OUTLINE",
                "POSITION_OUTLINE_INTENSITY",
                "INTENSITY",
            ],
            "mod_channel": {
                "B": "intensity",
                "C": "contrast",
                "S": "noise_scale",
            },
            "default_vals": {},
        },
        "WOOD": {
            "basis": "noise_basis_2",
            "type": "wood_type",
            "basis_list": [
                "SIN",
                "SAW",
                "TRI",
            ],
            "type_list": [
                "RINGNOISE",
                "BANDS",
                "RINGS",
                "BANDNOISE",
            ],
            "mod_channel": {
                "B": "intensity",
                "C": "contrast",
                "S": "noise_scale",
            },
            "default_vals": {},
        },
    }

    


    def __init__(self, context, args, op):
        super().__init__(context, args, op)
        self.texture_objects = []
        self.current_texture_index = 0
        self.transform_axis = "z"
        self.texture_adjust_channel = None
        self.inverted = 1
        self.rotating = False
        self.scaling = False
        self.vals_reset = True
    
    
    def initialize_modal(self, event):
        self.init_x = event.mouse_x
        self.init_y = event.mouse_y
        self.obj = self.get_active_obj()
        ### delete this after testing
        # self.init_tests(context)
        ###
        self.init_loc = self.obj.location
        self.init_rot = 0
        self.init_scale = 0
        self._init_coords_empty()
        self._init_modifier(self.context)
        self._init_textures()
        self.mod.texture = self.current_texture
        self.context.view_layer.objects.active = self.obj
        self.obj.select_set(True)
        # create collection for displace_coord objects
        colls = [coll.name for coll in bpy.data.collections[:]]
        self.active_coll = self.context.collection
        self.scene_coll = self.context.scene.collection
        self.dp_coll = utils.get_or_create_collection("DisplaceCoords")
        utils.link_collection(self.dp_coll)
        self.layer_coll = utils.find_layer_collection(self.dp_coll)
        self.layer_coll.hide_viewport = False
        empty_coll = self.empty.users_collection
        utils.transfer_obj_to_coll(self.empty, self.dp_coll, empty_coll[0])
    
    @property
    def curr_text_props(self):
        type = self.current_texture.type
        return self.texture_properties[type]

    @property
    def all_scene_disp_textures(self):
        d_textures = []
        for t in bpy.data.textures[:]:
            try:
                if t["is_displace"]:
                    d_textures.append(t)
            except KeyError:
                continue
        return d_textures

    def _init_textures(self):
        text_attrs = [t for t in self.textures if t]
        for name in text_attrs:
            text_name = f"Displace_{name}"
            textype = name.upper()
            tex = bpy.data.textures.new(text_name, textype)
            tex["is_displace"] = True
            props = self.texture_properties[textype]
            for chan in props["mod_channel"].values():
                val = getattr(tex, chan)
                self.texture_properties[textype]["default_vals"][chan] = val
            self.texture_objects.append(tex)
       

    @property
    def current_texture(self):
        return self.texture_objects[self.current_texture_index]

    def _init_coords_empty(self):
        bpy.ops.object.add(location=self.obj.location)
        self.empty = self.get_last_added_object()
        self.empty.name = "Displace_Coordinates"
        self.empty.empty_display_size = 0.1
        self.empty.empty_display_type = "SPHERE"

    def _init_modifier(self, context):
        context.view_layer.objects.active = self.obj
        bpy.ops.object.modifier_add(type="DISPLACE")
        self.mod = self._get_last_modifier()
        self.mod.texture_coords = "OBJECT"
        self.mod.texture_coords_object = self.empty
        self.mod.strength = 0

    def init_tests(self, context):
        texts = bpy.data.textures[:]
        for t in texts:
            bpy.data.textures.remove(t)
        for mod in self.obj.modifiers[:]:
            if mod.type == "DISPLACE":
                bpy.ops.object.modifier_remove(modifier=mod.name)
        try:
            mt = bpy.data.objects["Displace_Coordinates"]
            self.set_active_and_selected(context, mt)
            self.set_active_and_selected(context, self.obj, selected=False)
            bpy.ops.object.delete()
            self.set_active_and_selected(context, self.obj)
        except KeyError:
            pass

    def generate_msg(self):
        def get_float_fmt(items):
            return "\n".join([f"{amt:.2f}" for amt in items])

        rot_ax = self.transform_axis.upper()
        rot_amt = get_float_fmt(self.empty.rotation_euler)
        scale = get_float_fmt(self.empty.scale)[0]
        c_text = self.current_texture.type
        c_name = self.current_texture.name
        lines = [
            "MOVE: ALT",
            "ROTATE: CTRL",
            "SCALE: MOUSEWHEEL",
            f"ROTATION AXIS: {rot_ax}",
            f"ROTATION: {rot_amt}",
            f"SCALE: {scale}",
            f"TEXTURE_TYPE: {c_text}",
            f"TEXTURE_NAME: {c_name}",
        ]
        mod = self.mod_channel

        if mod is not None:
            chan = mod.upper().replace("_", " ")
            tac_msg = f"ADJUST CHANNEL: {chan}"
            lines.append(tac_msg)
        return ", ".join(lines)

    def get_mouse_val(self, event, multiplier, clamp_range=1):
        location = []
        for axis in list("xy"):
            init_loc = getattr(self, f"init_{axis}")
            mouse_loc = getattr(event, f"mouse_{axis}")
            val = (init_loc - mouse_loc) * multiplier
            loc = utils.clamp(val, -clamp_range, clamp_range)
            location.append(val)
        location.append(0.0)
        return Vector(location)

    def _new_texture_index(self, prev=False):
        if prev:
            addend = -1
        else:
            addend = 1
        return (self.current_texture_index + addend) % len(self.texture_objects)

    def _switch_textures(self, prev=False):
        new_index = self._new_texture_index(prev=prev)
        self.current_texture_index = new_index
        self.mod.texture = self.current_texture

    def set_adj_chan(self, channel=None):
        if self.texture_adjust_channel is None:
            self.texture_adjust_channel = channel
        elif self.mod_channel is None:
            self.texture_adjust_channel = None
        else:
            self.texture_adjust_channel = channel

    @property
    def mod_channel(self):
        props = self.curr_text_props
        opts = props["mod_channel"]
        channel = self.texture_adjust_channel
        try:
            return opts[channel]
        except KeyError:
            return None

    def adjust_channel(self, val):
        if self.mod_channel is not None:
            new_val = getattr(self.current_texture, self.mod_channel) + (val.x * 0.1)
            setattr(self.current_texture, self.mod_channel, new_val)

    def cleanup_textures(self):
        textures = bpy.data.textures[:]
        for tex in textures:
            if "Displace" in tex.name and tex.users == 0:
                bpy.data.textures.remove(tex)
        

    def change_texture_attr(self, attr_type="basis", prev=False):
        if prev:
            addend = -1
        else:
            addend = 1
        type = self.current_texture.type
        text = self.texture_properties[type]
        attr = text[attr_type]
        attr_list = self.texture_properties[type][f"{attr_type}_list"]
        current_attr = getattr(self.current_texture, attr)
        curr_index = attr_list.index(current_attr)
        new_index = (curr_index + addend) % len(attr_list)
        new_attr = attr_list[new_index]
        setattr(self.current_texture, attr, new_attr)


class AddDisplaceCustom(Operator):
    bl_idname = "object.custom_displace"
    bl_label = "Add Custom Displace"
    bl_options = {"REGISTER", "UNDO"}

    strength: bpy.props.FloatProperty()
    texture = bpy.props.StringProperty()
    size: bpy.props.FloatProperty()
    contrast: bpy.props.FloatProperty()

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == "MESH"

    def invoke(self, context, event):
        if context.mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")
        self.displacer = Displacer(context, self.as_keywords(), self)
        self.displacer.initialize_modal(event)
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        displacer = self.displacer
        msg = displacer.generate_msg()
        displacer.display_modal_info(msg, context)
        if event.shift:
            multiplier = 0.001
        else:
            multiplier = 0.01
        displacer.mod.strength = displacer.strength * displacer.inverted
        if event.type == "MOUSEMOVE":
            val = displacer.get_mouse_val(event, multiplier)
            displacer.adjust_channel(val)

            if event.alt:
                displacer.set_adj_chan()
                displacer.empty.location = displacer.init_loc + val
            elif displacer.rotating:
                displacer.set_adj_chan()
                setattr(
                    displacer.empty.rotation_euler,
                    displacer.transform_axis,
                    displacer.init_rot + val[0],
                )
            elif displacer.scaling:
                displacer.set_adj_chan()
                setattr(displacer.empty.scale, displacer.transform_axis, displacer.init_scale + val[0])
            else:
                val = (displacer.init_x - event.mouse_x) * multiplier
                displacer.strength = utils.clamp(val, -3, 3)

        # mousewheel adjust scale
        elif event.type in {"WHEELUPMOUSE", "WHEELDOWNMOUSE"}:
            scale_mod = (multiplier * 10) + 1
            if event.type == "WHEELUPMOUSE":
                displacer.empty.scale *= scale_mod
            else:
                displacer.empty.scale /= scale_mod
        elif event.value == "PRESS":
            e = event.type
            prev = False
            if event.shift:
                prev = True
            # switch texture type
            if e == "TAB":
                displacer._switch_textures(prev=prev)
            elif e == "Q":
                displacer.change_texture_attr(prev=prev)
            elif e == "W":
                displacer.change_texture_attr(attr_type="type", prev=prev)
            elif e == "E":
                if not displacer.vals_reset:
                    props = displacer.curr_text_props
                    for k, v in props["default_vals"].items():
                        setattr(displacer.current_texture, k, v)
                    displacer.set_adj_chan()
                    displacer.vals_reset = not displacer.vals_reset
            elif e == "S":
                if not displacer.scaling:
                    displacer.rotating = False
                displacer.scaling = not displacer.scaling
            elif e == "R":
                if not displacer.rotating:
                    displacer.scaling = False
                displacer.rotating = not displacer.rotating
            # change rotation axis
            elif e in list("XYZ"):
                displacer.transform_axis = event.unicode.lower()
            # change texture adjust channel
            elif e in list("BCDOLIT"):
                displacer.vals_reset = not displacer.vals_reset
                if displacer.texture_adjust_channel == e:
                    displacer.set_adj_chan()
                else:
                    displacer.set_adj_chan(e)
            # invert strength
            elif e == "N":
                displacer.inverted *= -1

        elif event.type == "LEFTMOUSE":
            e_name = re.sub("\.\d+", "", displacer.empty.name)
            displacer.empty.name = (
                f"{e_name}_{displacer.obj.name}_{displacer.current_texture.type.capitalize()}"
            )
            displacer.layer_coll.hide_viewport = True
            displacer._clear_info(context)
            displacer.cleanup_textures()
            del displacer
            return {"FINISHED"}
        elif event.type in {"RIGHTMOUSE", "ESC"}:
            displacer._clear_info(context)
            bpy.ops.object.modifier_remove(modifier=displacer.mod.name)
            displacer.cleanup_textures()
            displacer.dp_coll.objects.unlink(displacer.empty)
            if len(displacer.dp_coll.objects[:]) == 0:
                displacer.scene_coll.children.unlink(displacer.dp_coll)
            del displacer
            return {"CANCELLED"}
        return {"RUNNING_MODAL"}
