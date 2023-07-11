import bpy
from custom_operator import *


def is_widget(obj):
    return obj.type == "MESH" and "WGT" in obj.name


def create_wgt_collection():
    coll_exists = False
    try:
        coll = bpy.data.collections["wgts"]
    except KeyError:
        coll = bpy.data.collections.new("wgts")
    return coll


def coll_index():
    for i, coll in enumerate(bpy.data.collections[:]):
        print(i, coll)
        if coll.name == "wgts":
            return i


def move_objects(context):
    coll = create_wgt_collection()
    for obj in bpy.data.objects[:]:
        if is_widget(obj):
            user_col = obj.users_collection[0]
            user_col.objects.unlink(obj)
            coll.objects.link(obj)

    coll.hide_viewport = True


class OBJECT_OT_move_wgts_to_collection(bpy.types.Operator):
    bl_idname = "object.move_widgets_to_collection"
    bl_label = "Hide WGT Objects"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        move_objects(context)
        return {"FINISHED"}


def hide_widget_objects_menu_func(self, context):
    layout = self.layout
    layout.operator("object.move_widgets_to_collection")


def register():
    bpy.types.VIEW3D_MT_object.append(hide_widget_objects_menu_func)


def unregister():
    bpy.types.VIEW3D_MT_object.remove(hide_widget_objects_menu_func)
