import bpy
from bpy.types import Operator


class CollisionGenerator:

    def __init__(self, context, obj):
        self.context = context
        self.obj = obj 
        self.mesh = obj.data
        

    @staticmethod
    def make_convex_hull():
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.convex_hull()
        bpy.ops.object.mode_set(mode="OBJECT")

    def duplicate_obj(self):
        self.copy_mesh = self.mesh.copy()
        self.copy_obj = bpy.data.objects.new(f"{self.obj.name}_Collision",object_data=self.copy_mesh)
        coll = self.context.collection
        coll.objects.link(self.copy_obj)
        self.copy_obj.location = self.obj.location.copy()
        self.context.view_layer.objects.active = self.copy_obj
        self.copy_obj.select_set(True)

    def add_decimate(self):
        dec = self.copy_obj.modifiers.new('CollisionDecimate', type="DECIMATE")
        dec.ratio = .15
        dec.decimate_type = "COLLAPSE"

    def set_collision_name_and_collection(self):
        self.obj.select_set(True)
        self.copy_obj.select_set(True)
        self.context.view_layer.objects.active = self.obj
        bpy.ops.object.set_collision_name_from_active()
        self.obj.select_set(False)
        self.context.view_layer.objects.active = None
        self.copy_obj.select_set(False)

    def generate_collision(self):
        self.obj.select_set(False)
        self.duplicate_obj()
        self.make_convex_hull()
        self.add_decimate()
        self.set_collision_name_and_collection()


class OBJECT_OT_generate_collision_object( Operator):
    bl_idname = "object.generate_collision_object"
    bl_label = "Generate Collision Objects"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.selected_objects
    
    def execute(self, context):
        objects = context.selected_objects[:]
        for obj in context.selected_objects:
            obj.select_set(False)
        for obj in objects:
            if obj.type == "MESH":
                cg = CollisionGenerator(context, obj)
                cg.generate_collision()
                del cg
        return {"FINISHED"}

