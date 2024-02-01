from bpy.types import Operator
from custom_operator import *


class OBJECT_OT_deselect_parented_objs(CustomOperator, Operator):
    bl_idname = "object.deselect_parented_objs"
    bl_label = "Deselect Parented Objs"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objs = context.selected_objects
        for obj in objs[:]:
            constraints = [const.type for const in obj.constraints]
            if obj.parent or "CHILD_OF" in constraints:
                obj.select_set(False)
        return {"FINISHED"}


def deselect_parented_objs_menu_func(self, context):
    layout = self.layout
    layout.operator("object.deselect_parented_objs")


def register():
    bpy.types.VIEW3D_MT_select_object.append(deselect_parented_objs_menu_func)


def unregister():
    bpy.types.VIEW3D_MT_select_object.remove(deselect_parented_objs_menu_func)
