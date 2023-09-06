import bpy
from bpy.props import IntProperty, FloatProperty
from mathutils import Vector, Matrix
import mathutils
import bmesh
import numpy as np


class Primitive:

    def __init__(self, context, bm, mesh, obj):
        self.context = context 
        self.mode = context.mode
        self.bm = bm
        self.obj = obj
        self.mesh = mesh
        self.geom = []
        self.origin = None
        self.rot_matrix = None
        if self.bm.select_history.active:
            self.align_to_active = True
        else:
            self.align_to_active = False

    @property
    def cursor_loc(self):
        return self.context.scene.cursor.location.copy()

    @staticmethod
    def get_geom_from_geom_dict(geom_dict, kw="geom"):
        return [v for v in geom_dict[kw] if isinstance(v, bmesh.types.BMVert)]
    
    def get_rotation_matrix_from_face(self):
        active_face = self.bm.select_history.active
        if active_face is None:
            return self.context.scene.cursor.matrix.copy()
        z = active_face.normal
        x = active_face.calc_tangent_edge()
        y = np.cross(x, z)
        mat = mathutils.Matrix([x, y, z]).to_4x4()
        return mat
    
    def flip_faces(self, verts):
        for face in self.bm.faces[:]:
            for vert in face.verts[:]:
                if vert in verts:
                    face.normal_flip()
                    break

    def get_origin_from_active_face(self):
        active_face = self.bm.select_history.active
        if active_face is not None:
            return active_face.calc_center_median()
        return self.cursor_loc
    
    def set_primitive_location(self):
        if self.mode == "OBJECT" or not self.align_to_active:
            self.origin = self.cursor_loc
        else:
            self.origin = self.get_origin_from_active_face()

    def set_primitive_rotation(self):
        if self.mode == "OBJECT" or not self.align_to_active:
            self.rot_matrix = self.context.scene.cursor.matrix.copy()
        else:
            self.rot_matrix = self.get_rotation_matrix_from_face()

    
    def get_faces_of_verts(self, verts):
        faces = set()
        for face in self.bm.faces[:]:
            for vert in face.verts[:]:
                if vert in verts:
                    faces.add(face)
                    break

        return list(faces)
    

    
    def get_additional_transform_matrix(self):
        return Vector([0, 0, 0])
    

    def create_mesh(self):
        self.bm.select_flush(True)
        self.set_primitive_location()
        self.set_primitive_rotation()

        # matrix for added geo
        mat = Matrix()
        mat.translation = self.origin
        # rotate geo matrix
        mat = mat @ self.rot_matrix.inverted()
        # get matrix for translating cube up by half of height
        trans_local = self.get_additional_transform_matrix()
        trans_world = mat.to_3x3() @ trans_local
        mat.translation += trans_world
        # bmesh.ops.create_cube(bm, size=cube_size, matrix=mat)
        self.generate_primitive()

        bmesh.ops.transform(self.bm, matrix=mat, verts=self.geom)
        
    
    def generate_primitive(self):
        return list()
    
    def do_primitive_action(self):
        self.create_mesh()
        if self.mode == "OBJECT":
            self.bm.to_mesh(self.mesh)
        else:
            bmesh.update_edit_mesh(self.mesh)

    def finalize_primitive(self):
        if self.mode == "EDIT_MESH":
            for vert in self.bm.verts:
                if vert in self.geom:
                    vert.select_set(True)
            active_face =  self.bm.select_history.active
            if active_face:
                active_face.select_set(False)
            self.bm.select_flush(True)
            bmesh.update_edit_mesh(self.mesh)
    
    def cancel_operation(self):
        bmesh.ops.delete(self.bm, geom=self.geom)
        bmesh.update_edit_mesh(self.mesh)
        if self.mode == "OBJECT":
            bpy.data.objects.remove(self.obj)
            bpy.data.meshes.remove(self.mesh)

        
        
    

    

class CubePrimitive(Primitive):

    def __init__(self, *args, height=0.5):
        super().__init__(*args)
        self.height = height 

    def generate_primitive(self):
        if self.geom:
            bmesh.ops.delete(self.bm, geom=self.geom)
        geom = bmesh.ops.create_cube(self.bm, size=self.height, matrix=self.rot_matrix)
        self.geom = geom['verts']

    def get_additional_transform_matrix(self):
        return Vector([0,0, self.height / 2.0])
    

    
class CylinderPrimitive(Primitive):

    def __init__(self, *args, height=0.5, segments=8.0, radius=.25):
        super().__init__(*args)
        self.init_height = height
        self.init_radius = radius
        self.height = height 
        self.radius = radius 
        self.segments = segments

    def debug_message(self, set_val, event):
        print(f"""*CYLINDER*:
              HEIGHT: {self.height}
              RADIUS: {self.radius}
              SEGMENTS: {self.segments}
              SET_VAL: {set_val} 
              EVENT: {event.mouse_x, event.mouse_y}
              """
              )

    def generate_primitive(self):
        if self.geom:
            bmesh.ops.delete(self.bm, geom=self.geom)
        self.create_cylinder()

    def create_cylinder(self):
        height_vec = Vector([0, 0, self.height])
        base_circle = bmesh.ops.create_circle(
            self.bm, cap_ends=True, segments=self.segments, radius=self.radius
        )
        bc_verts = base_circle["verts"]
        faces = self.get_faces_of_verts(bc_verts)
        top = bmesh.ops.extrude_face_region(self.bm, geom=faces)
        top_verts = self.get_geom_from_geom_dict(top)
        bmesh.ops.translate(self.bm, vec=height_vec, verts=top_verts)
        bc_verts.extend(top_verts)
        if self.mode == "EDIT_MESH" and self.align_to_active:
            self.flip_faces(bc_verts)
        self.geom = bc_verts

    def set_modal_size_values(self, event, x_value, y_value):
        if event.ctrl:
            
            self.height =  x_value
        else:
            self.radius = x_value

        

        self.debug_message(x_value, event)

    def set_segment_value(self, event):
        if event.type == "WHEELUPMOUSE":
            self.segments += 1
        elif event.type == "WHEELDOWNMOUSE":
            self.segments = max(self.segments - 1, 3)



    
class OBJECT_OT_create_cylinder_modal(bpy.types.Operator):
    bl_idname = "object.create_cylinder_modal"
    bl_label = "Create Cylinder Modal"
    bl_options = {"REGISTER", "UNDO"}

    segments: IntProperty(min=3, default=8)
    height: FloatProperty(default=0)
    radius: FloatProperty(default=0)

    def set_delta_mouse_val(self, event):
        x_val = event.mouse_x
        multiplier = .01
        if event.shift:
            multiplier *= .1
         
        init_loc = Vector([self.init_mouse_loc_x, self.init_mouse_loc_y])
        curr_loc = Vector([event.mouse_region_x, event.mouse_region_y])
        value = (curr_loc - init_loc ).length
        # self.curr_x = self.multiplier * (event.mouse_x - self.curr_x)
        # self.curr_y = self.multiplier * (event.mouse_y - self.curr_y)
        self.curr_x = multiplier * value


    def modal(self, context, event):
        
        if event.type in  {"WHEELUPMOUSE", "WHEELDOWNMOUSE"}:
            self.cylinder_primitive.set_segment_value(event) 

        elif event.type == "MOUSEMOVE":
            self.set_delta_mouse_val(event)
            if event.ctrl:
                self.current_adjustment_mode = "HEIGHT"
            
            self.cylinder_primitive.set_modal_size_values(event, self.curr_x, self.curr_x)

        elif event.type in {"ESC", "RIGHTMOUSE"}:
            self.cylinder_primitive.cancel_operation()
            return {"CANCELLED"}

        elif event.type == "LEFTMOUSE":
            self.cylinder_primitive.finalize_primitive()
            self.obj.select_set(True)
            context.view_layer.objects.active = self.obj
            return {"FINISHED"}

        self.cylinder_primitive.do_primitive_action()
        return {"RUNNING_MODAL"}
    
    def invoke(self, context, event):
        if context.mode == "OBJECT":
            mesh = bpy.data.meshes.new(name="Cylinder")
            obj = bpy.data.objects.new(name="Cylinder", object_data=mesh)
            context.collection.objects.link(obj)
            bm = bmesh.new()
            
        elif context.mode == "EDIT_MESH":
            obj = context.edit_object
            mesh = obj.data
            bm = bmesh.from_edit_mesh(mesh)

        self.cylinder_primitive = CylinderPrimitive(
            context, 
            bm, 
            mesh,
            obj,
            segments=self.segments,
            height=self.height,
            radius=self.radius,

            )
        self.scale_adjustment = 1.0
        self.current_adjustment_mode = "RADIUS"
        self.obj = obj
        self.init_mouse_loc_x = event.mouse_x
        self.init_mouse_loc_y = event.mouse_y
        self.curr_x = event.mouse_x
        self.curr_y = event.mouse_y

        self.context = context
        self.mode = context.mode
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}
        




# def get_matrix_from_face(face: bmesh.types.BMFace):
#     z = face.normal
#     x = face.calc_tangent_edge()
#     y = np.cross(x, z)
#     mat = mathutils.Matrix([x, y, z]).to_4x4()
#     return mat


# class OBJECT_OT_create_cylinder_modal(bpy.types.Operator):
#     bl_idname = "object.create_cylinder_modal"
#     bl_label = "Create Cylinder Modal"
#     bl_options = {"REGISTER", "UNDO"}

#     segments: IntProperty(min=3)
#     height: FloatProperty()
#     radius: FloatProperty()

#     def add_edit_mode_mesh(self):
#         self.bm.select_flush(True)
#         face = self.bm.select_history.active

#         origin = face.calc_center_median()
#         rot_mat = get_matrix_from_face(face)

#         # matrix for added geo
#         mat = Matrix()
#         mat.translation = origin
#         # rotate geo matrix
#         mat = mat @ rot_mat.inverted()
#         # get matrix for translating cube up by half of height
#         trans_local = Vector([0, 0, 0])
#         trans_world = mat.to_3x3() @ trans_local
#         mat.translation += trans_world

#         # bmesh.ops.create_cube(bm, size=cube_size, matrix=mat)
#         cv = self.create_cylinder_mesh()

#         bmesh.ops.transform(self.bm, matrix=mat, verts=cv)
#         bmesh.update_edit_mesh(self.mesh)

#     def get_geom_from_geom_dict(self, geom_dict, kw="geom"):
#         return [v for v in geom_dict[kw] if isinstance(v, bmesh.types.BMVert)]

#     def get_faces_of_verts(self, verts):
#         faces = set()
#         for face in self.bm.faces[:]:
#             for vert in face.verts[:]:
#                 if vert in verts:
#                     faces.add(face)
#                     break

#         return list(faces)

#     def flip_faces(self, verts):
#         for face in self.bm.faces[:]:
#             for vert in face.verts[:]:
#                 if vert in verts:
#                     face.normal_flip()
#                     break

#     def create_cylinder_mesh(self):
#         if self.created_geo:
#             bmesh.ops.delete(self.bm, geom=self.created_geo)
#         height_vec = Vector([0, 0, self.height])
#         base_circle = bmesh.ops.create_circle(
#             self.bm, cap_ends=True, segments=self.segments, radius=self.radius
#         )
#         bc_verts = base_circle["verts"]
#         faces = self.get_faces_of_verts(bc_verts)
#         top = bmesh.ops.extrude_face_region(self.bm, geom=faces)
#         top_verts = self.get_geom_from_geom_dict(top)
#         bmesh.ops.translate(self.bm, vec=height_vec, verts=top_verts)
#         bc_verts.extend(top_verts)
#         if self.mode == "EDIT_MESH":
#             self.flip_faces(bc_verts)
#         self.created_geo = bc_verts

#         return bc_verts

#     def add_cylinder(self, context):
#         if context.mode == "OBJECT":
#             self.create_cylinder_mesh()
#             self.bm.to_mesh(self.mesh)
#         else:
#             self.add_edit_mode_mesh()
#             bmesh.update_edit_mesh(self.mesh)

#     def modal(self, context, event):
#         if event.type == "WHEELUPMOUSE":
#             self.segments += 1

#         elif event.type == "WHEELDOWNMOUSE":
#             self.segments = max(self.segments - 1, 3)

#         elif event.type in {"ESC", "RIGHTMOUSE"}:
#             return {"CANCELLED"}

#         elif event.type == "LEFTMOUSE":
#             if self.mode == "EDIT_MESH":
#                 for vert in self.bm.verts:
#                     if vert in self.created_geo:
#                         vert.select_set(True)
#                 self.bm.select_history.active.select_set(False)
#                 self.bm.select_flush(True)
#                 bmesh.update_edit_mesh(self.mesh)
#             else:
#                 self.obj.select_set(True)
#                 context.view_layer.objects.active = self.obj
#             return {"FINISHED"}

#         self.add_cylinder(context)

#         return {"RUNNING_MODAL"}

#     def invoke(self, context, event):
#         if context.mode == "OBJECT":
#             mesh = bpy.data.meshes.new(name="Cylinder")
#             obj = bpy.data.objects.new(name="Cylinder", object_data=mesh)
#             context.collection.objects.link(obj)
#             obj.location = context.scene.cursor.location.copy()
#             bm = bmesh.new()
#             self.obj = obj
#         elif context.mode == "EDIT_MESH":
#             obj = context.edit_object
#             mesh = obj.data
#             bm = bmesh.from_edit_mesh(mesh)

#         self.context = context
#         self.mode = context.mode
#         self.created_geo = []
#         self.mesh = mesh
#         self.bm = bm
#         self.segments = 8
#         self.height = 1
#         self.radius = 0.5

#         context.window_manager.modal_handler_add(self)
#         return {"RUNNING_MODAL"}
