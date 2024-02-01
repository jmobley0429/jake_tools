# modifier

import bpy
import numpy as np
import utils
from bpy.types import Operator
from custom_operator import *


class CustomDataTransferModifier(CustomOperator):
    def __init__(self, context, args, op):
        self._set_args(args)
        self.context = context
        self.operator = op

    def _make_dt_object_collection(self):
        coll = utils.get_or_create_blender_data_block(
            "collections", "data_transfer_objs"
        )
        utils.link_collection(coll)
        coll.objects.link(self.active_obj)
        root_coll = utils.find_objects_collection(self.active_obj)
        root_coll.objects.unlink(self.active_obj)

    def _get_objs(self):
        all_objs = self.context.selected_objects[:]
        sel_objs = []
        self.active_obj = self.context.active_object
        if self.active_obj is not None:
            for obj in all_objs:
                if obj != self.active_obj:
                    sel_objs.append(obj)
        else:
            sel_objs = all_objs
        self.sel_objs = sel_objs

    def _add_mod(self, obj):
        return obj.modifiers.new("DataTransfer", "DATA_TRANSFER")

    def _get_vertex_groups(self, obj):
        good_names = [
            "dt",
            "data",
            "data_transfer",
            "datatransfer",
            "trans",
            "transfer",
            "data_trans",
        ]
        for group in obj.vertex_groups[:]:
            if group.name.lower() in good_names:
                return group

    def _set_target_object_atrributes(self):
        mod_object_name = self.sel_objs[0].name
        self.active_obj.display_type = "WIRE"
        self.active_obj.name = f"{mod_object_name}_dt_target"

    def _add_child_of_constraint(self):
        for obj in self.sel_objs:
            consts = [c.type for c in obj.constraints]
            if "CHILD_OF" not in consts:
                co = obj.constraints.new(type="CHILD_OF")
                co.target = self.active_obj

    def execute(self):
        self._get_objs()
        if self.active_obj is None:
            for obj in self.sel_objs:
                self._add_mod(obj)
        else:
            for obj in self.sel_objs:
                mod = self._add_mod(obj)
                mod.use_loop_data = True
                mod.data_types_loops = {"CUSTOM_NORMAL"}
                mod.loop_mapping = "POLYINTERP_NEAREST"
                mod.object = self.active_obj
                v_group = self._get_vertex_groups(obj)
                if v_group is not None:
                    mod.vertex_group = v_group.name
                # self._add_child_of_constraint()
        if self.hide_target:
            self._set_target_object_atrributes()
            self._make_dt_object_collection()
        return {"FINISHED"}


class OBJECT_OT_CustomDataTransferModifier(bpy.types.Operator):
    bl_idname = "object.custom_dt_modifier_add"
    bl_label = "Data Transfer"
    bl_description = "Adds Data Transfer Modifiers"
    bl_options = {"REGISTER", "UNDO"}

    hide_target: bpy.props.BoolProperty("Hide Target", default=True)

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects)

    def invoke(self, context, event):
        if event.alt:
            self.hide_target = False
        return self.execute(context)

    def execute(self, context):
        args = self.as_keywords()
        dtmod = CustomDataTransferModifier(context, args, self)
        return dtmod.execute()
