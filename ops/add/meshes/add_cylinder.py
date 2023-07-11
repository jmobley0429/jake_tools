import bpy
import bmesh
from bpy_extras.object_utils import AddObjectHelper
from bpy_extras import object_utils
from mathutils import Vector
from jake_tools.ops.custom_operator import *



class CustomCylinderAdd(CustomBmeshOperator, bpy.types.Operator, AddObjectHelper):
    """Add a simple cylinder mesh"""

    bl_idname = "mesh.custom_cylinder_add"
    bl_label = "Add Cylinder"
    bl_options = {'REGISTER', 'UNDO'}

    radius: bpy.props.FloatProperty(
        name="Radius",
        description="Cylinder Radius",
        default=0.5,
    )
    height: bpy.props.FloatProperty(
        name="Height",
        description="Cylinder Height",
        default=1.0,
    )
    vertices: bpy.props.IntProperty(
        name="Vertices",
        description="Vertex Count",
        default=16,
    )

    center_origin = True

    def invoke(self, context, event):
        if event.alt:
            self.center_origin = False
        return self.execute(context)

    def execute(self, context):
        self.new_bmesh("Cylinder")
        bmesh.ops.create_circle(self.bm, cap_ends=True, radius=self.radius, segments=self.vertices)
        faces = self.bm.faces[:]
        ret = bmesh.ops.extrude_face_region(self.bm, geom=faces)
        new_verts = [v for v in ret['geom'] if self.is_vert(v)]
        del ret
        vec = Vector((0, 0, self.height))
        bmesh.ops.translate(
            self.bm,
            vec=vec,
            verts=new_verts,
        )
        if self.center_origin:
            translate = self.height / 2
            for vert in self.bm.verts[:]:
                vert.co.z -= translate

        self.bm.to_mesh(self.mesh)
        self.mesh.update()
        object_utils.object_data_add(context, self.mesh, operator=self)
        return {'FINISHED'}