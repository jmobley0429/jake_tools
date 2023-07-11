import bpy
import re
from bpy.types import Operator
from custom_operator import *


class DuplicateObjectDeleter(OperatorBaseClass):
    def __init__(self, context, args, op):
        super().__init__(context, args, op=op)
        self.ids = []
        self.all_objs = []
        self.dupe_objs = []
        self.good_objs = []
        self.deps = self.context.evaluated_depsgraph_get()

    def _has_same_verts(self, obj, dupe):
        print("comparing objs: ", obj.name, dupe.name)
        obj = obj.evaluated_get(self.deps)
        dupe = dupe.evaluated_get(self.deps)
        same_verts = len(dupe.data.vertices[:]) == len(obj.data.vertices[:])
        print("Has same verts: ", same_verts)
        return same_verts

    def get_obj_name(self, obj):
        return re.split("\.|(_)\d{2}", obj.name)[0]

    def get_obj_id(self, obj):
        loc = obj.location
        name = self.get_obj_name(obj)
        return (loc, name)

    def delete_dupe_objects(self):
        sel_objs = self.context.selected_objects[:]
        for obj in sel_objs:
            if obj.type == "MESH":
                self.all_objs.append(obj)
        duped_objs = []
        for obj in sel_objs:
            if obj.type == "MESH":
                id1 = self.get_obj_id(obj)
                for check_obj in self.all_objs[:]:
                    if check_obj != obj:
                        id2 = self.get_obj_id(check_obj)
                        if (
                            id1 == id2
                            and self._has_same_verts(obj, check_obj)
                            and check_obj not in self.good_objs
                        ):
                            duped_objs.append(check_obj)
                        else:
                            self.good_objs.append(obj)

        self.op.report({"INFO"}, f"Finished. {len(duped_objs)} deleted.")
        for del_obj in duped_objs[:]:
            try:
                bpy.data.objects.remove(del_obj)
            except ReferenceError:
                print(f"couldn't delete: {del_obj.name}")
        return {"FINISHED"}


class OBJECT_OT_RemoveDoubledObjects(Operator):
    bl_idname = "object.remove_doubled_objects"
    bl_label = "Remove Doubled Objects"
    desc_lines = [
        "Loop over selected objects and delete objects",
        "that share the same location and name w/o suffix.",
    ]
    bl_description = "\n".join(desc_lines)
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 1

    def execute(self, context):
        args = self.as_keywords()
        dod = DuplicateObjectDeleter(context, args, op=self)
        return dod.delete_dupe_objects()