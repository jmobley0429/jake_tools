import bpy
from bpy.types import Operator
from custom_operator import *
import numpy as np
from mathutils import Vector


class AlignOperator:
    axis: bpy.props.EnumProperty(
        name="Axis",
        description="Alignment Axis",
        items=[
            ("x", "X", "X-Axis"),
            ("y", "Y", "Y-Axis"),
            ("z", "Z", "Z-Axis"),
        ],
        default="x",
    )
    align_to: bpy.props.EnumProperty(
        name="Axis",
        description="Where to align selected objects",
        items=[
            ("NEG", "Negative", "Negative"),
            ("POS", "Positive", "Positive"),
            ("CURSOR", "Cursor", "Cursor"),
            ("ACTIVE", "Active", "Active"),
            ("GRID", "Active", "Active"),
            ("ROW", "Row", "Row"),
        ],
        default="GRID",
    )

    axes = list("xyz")

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.selected_objects

    def get_new_loc_tuple(self, loc):
        coord = [0] * 3
        index = self.axes.index(self.axis)
        coord[index] = loc
        return Vector(coord)

    def get_objs(self, context):
        return [obj for obj in context.selected_objects if obj.parent is None]


class OBJECT_OT_sort_items_on_axis(AlignOperator, CustomModalOperator, Operator):
    bl_idname = "object.sort_objects_on_axis"
    bl_label = "Sort Objects on Axis"
    bl_options = {"REGISTER", "UNDO"}

    spacing_multiplier: bpy.props.FloatProperty(name="Spacing", default=1.5)
    grid_offset: bpy.props.IntProperty(name="Grid Offset", default=6)
    grid_axis: bpy.props.EnumProperty(
        name="Grid Axis",
        description="Axis on which to array items on a grid",
        items=[
            ("x", "X", "X-Axis"),
            ("y", "Y", "Y-Axis"),
            ("z", "Z", "Z-Axis"),
        ],
        default="y",
    )

    def get_obj_dim(self, obj):
        return getattr(obj.dimensions, self.axis)

    def get_grid_offset(self):
        return max([self.get_obj_dim(obj) for obj in self.objs])

    def set_grid_offset(self, addend):
        self.grid_offset = np.clip(self.grid_offset + addend, 1, self.num_objs)

    @property
    def prev_obj(self):
        if self.current_index == 0:
            return self.objs[0]
        else:
            return self.objs[self.current_index - 1]

    @property
    def current_obj(self):
        return self.objs[self.current_index]

    @property
    def axis_string(self):
        return str(self.axis).upper().strip()

    @property
    def grid_axis_string(self):
        return str(self.grid_axis).upper().strip()

    @property
    def modal_info_string(self):
        if self.sort_asc is not None:
            type = "Descending"
            if self.sort_asc:
                type = "Ascending"
        else:
            type = "None"
        msg = [
            f"(Tab) AXIS: {self.axis_string}",
            f"(Mousewheel) SPACING MULTIPLIER: {self.spacing_multiplier:.2f}",
            f"(Ctrl + Mousewheel) GRID OFFSET: {self.grid_offset}",
            f"(G) GRID AXIS: {self.grid_axis_string}",
            f"(S) Sort Type: {type}",
        ]
        return ", ".join(msg)

    def calc_obj_loc(self):
        obj_dim = self.get_obj_dim(self.current_obj)
        prev_dim = self.get_obj_dim(self.prev_obj)
        return self.get_new_loc_tuple(
            ((obj_dim + prev_dim) / 2) * self.spacing_multiplier
        )

    def cycle_axis(self, event, axis, axis_type="axis"):
        current_axis_index = self.axes.index(axis)
        if event.shift:
            new_ax = self.axes[current_axis_index - 1]
        else:
            new_ax = self.axes[(current_axis_index + 1) % len(self.axes)]
        setattr(self, axis_type, new_ax)

    def cycle_sort_asc(self, event):
        types = [None, False, True]
        current_type_index = types.index(self.sort_asc)
        if event.shift:
            new_type = types[current_type_index - 1]
        else:
            new_type = types[(current_type_index + 1) % len(self.axes)]
        setattr(self, "sort_asc", new_type)

    def arrange_objs(self, context):
        first_loc = self.initial_loc.copy()
        self.current_index = 0
        for obj in self.objs:
            # print(f"Arranging {obj.name}")
            if self.current_index == 0:
                obj.location = first_loc
            else:
                new_loc = self.calc_obj_loc()
                first_loc += new_loc
                # print(f"First loc after x mod: {first_loc}")
                if self.current_index % self.grid_offset == 0:
                    old_ax = self.axis
                    self.axis = self.grid_axis
                    grid_loc = self.get_new_loc_tuple(self.get_grid_offset())
                    old_axis_orig = getattr(self.cursor_loc, old_ax)
                    # print(f"OLD:{old_axis_orig}")
                    setattr(first_loc, old_ax, old_axis_orig)
                    first_loc += grid_loc
                    # print(f"GRID_LOC: {grid_loc}, FIRST_LOC: {first_loc}")
                    self.axis = old_ax
                obj.location = first_loc
            self.current_index += 1
        del first_loc

    def sort_objs_size(self, average=True):
        def get_obj_dims(obj):
            if average:
                return np.mean(obj.location)
            else:
                return getattr(obj.location, self.axis)

        if self.sort_asc is None:
            return self.original_obj_list
        return sorted(
            self.objs, key=lambda obj: get_obj_dims(obj), reverse=self.sort_asc
        )

    def invoke(self, context, event):
        self.initial_loc = Vector((0, 0, 0))
        self.sort_asc = None
        self.objs = self.get_objs(context)
        self.original_obj_list = self.objs.copy()
        if event.alt:
            self.sort_asc = True
        elif event.ctrl:
            self.sort_asc = False
        self.objs = self.sort_objs_size()
        self.original_locations = [obj.location.copy() for obj in self.objs]
        self.num_objs = len(self.objs)
        self.cursor_loc = context.scene.cursor.location.copy()
        if self.align_to != "GRID":
            self.grid_offset = self.num_objs
            self.initial_loc = self.cursor_loc.copy()
            if self.align_to == "ACTIVE":
                self.initial_loc = context.active_object.location.copy()
            elif self.align_to in {"NEG", "POS"}:
                locs = sorted(
                    self.original_locations, key=lambda x: getattr(x, self.axis)
                )
                self.initial_loc = locs[-1]
                if self.align_to == "NEG":
                    self.initial_loc = locs[0]
            self.arrange_objs(context)
            return {"FINISHED"}
        else:
            self.grid_offset = int(self.num_objs // 2.5)
            self.spacing_multiplier = 1.9
            self.arrange_objs(context)
            context.window_manager.modal_handler_add(self)
            return {"RUNNING_MODAL"}

    def modal(self, context, event):
        self.display_modal_info(self.modal_info_string, context)
        if event.value == "PRESS":
            if event.type == "TAB":
                self.cycle_axis(event, axis=self.axis)
            elif event.type == "G":
                self.cycle_axis(event, axis=self.grid_axis, axis_type="grid_axis")
            elif event.type == "WHEELUPMOUSE":
                if event.ctrl:
                    self.set_grid_offset(1)
                else:
                    self.spacing_multiplier += 0.1
            elif event.type == "WHEELDOWNMOUSE":
                if event.ctrl:
                    self.set_grid_offset(-1)
                else:
                    self.spacing_multiplier -= 0.1
            elif event.type in {"RIGHTMOUSE", "ESC"}:
                objs = self.get_objs(context)
                for obj, loc in zip(objs, self.original_locations):
                    obj.location = loc
                return self.exit_modal(context, cancelled=True)
            elif event.type == "LEFTMOUSE":
                return self.exit_modal(context)
            elif event.type == "S":
                self.cycle_sort_asc(event)
                self.objs = self.sort_objs_size()
            self.arrange_objs(context)
        return {"RUNNING_MODAL"}


class OBJECT_OT_align_objects(AlignOperator, Operator):
    bl_idname = "object.align_objects"
    bl_label = "Align Objects"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        self.objs = self.get_objs(context)
        self.active_obj = context.active_object
        locs = [obj.location.copy() for obj in self.objs]
        if self.align_to in {"NEG", "POS"}:
            locs = [getattr(loc, self.axis) for loc in locs]
            if self.align_to == "NEG":
                self.align_loc = self.get_new_loc_tuple(min(locs))
            else:
                self.align_loc = self.get_new_loc_tuple(max(locs))
        elif self.align_to == "CURSOR":
            self.align_loc = context.scene.cursor.location.copy()
        else:
            self.align_loc = context.active_object.location.copy()

        return self.execute(context)

    def execute(self, context):
        loc_val = getattr(self.align_loc, self.axis)
        for obj in self.objs:
            setattr(obj.location, self.axis, loc_val)
        return {"FINISHED"}


# kms = [
#     {
#         "keymap_operator": OBJECT_OT_align_objects.bl_idname,
#         "name": "Object Mode",
#         "letter": "X",
#         "shift": 0,
#         "ctrl": 0,
#         "alt": 1,
#         "space_type": "VIEW_3D",
#         "region_type": "WINDOW",
#         "keywords": {},
#     },
#     {
#         "keymap_operator": OBJECT_OT_sort_items_on_axis.bl_idname,
#         "name": "Object Mode",
#         "letter": "O",
#         "shift": 1,
#         "ctrl": 0,
#         "alt": 1,
#         "space_type": "VIEW_3D",
#         "region_type": "WINDOW",
#         "keywords": {},
#     },
# ]
