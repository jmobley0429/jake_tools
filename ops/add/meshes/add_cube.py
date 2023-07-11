import bpy
import bmesh
from bpy_extras.object_utils import AddObjectHelper
from bpy_extras import object_utils
from mathutils import Euler
from pathlib import Path
from jake_tools.ops.custom_operator import *



class CustomCubeAdd(CustomBmeshOperator, bpy.types.Operator, AddObjectHelper):
    """Add a simple cube mesh"""

    bl_idname = "mesh.custom_cube_add"
    bl_label = "Add Cube"
    bl_options = {'REGISTER', 'UNDO'}

    size: bpy.props.FloatProperty(
        name="Size",
        description="Cube Size",
        min=0.01,
        max=100.0,
        default=1.0,
    )

    center_origin = True

    def invoke(self, context, event):
        if event.alt:
            self.center_origin = False
        return self.execute(context)

    def execute(self, context):
        self.new_bmesh("Cube")
        geom = bmesh.ops.create_cube(self.bm, size=self.size)
        if not self.center_origin:
            translate = self.size / 2
            for vert in geom['verts']:
                vert.co.z += translate
        self.bm.to_mesh(self.mesh)
        self.mesh.update()
        object_utils.object_data_add(context, self.mesh, operator=self)
        return {'FINISHED'}