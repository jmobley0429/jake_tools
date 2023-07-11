import bpy 
import utils 
import bmesh





def is_boundary(edge, faces):
    link_faces = set(edge.link_faces[:])
    num_link_intersect = len(link_faces.intersection(faces))
    return num_link_intersect == 1


def select_non_boundary(context):
    edit_obj = context.edit_object
    mesh = edit_obj.data
    bm = bmesh.from_edit_mesh(mesh)
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
    faces = set([f for f in bm.faces if f.select])
    for e in bm.edges[:]:
       if e.select and is_boundary(e, faces):
            e.select_set(False)
    bm.select_flush(False)
    bmesh.update_edit_mesh(mesh)



class MESH_OT_select_boundary_loops(bpy.types.Operator):
    bl_idname = "mesh.select_boundary_loops"
    bl_label = "Select Boundary Loops"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = 'Select Boundary Loop, ALT > Select all non-boundary loops.'

    select_non_boundary: bpy.props.BoolProperty(name="Non Boundary?", default=False,)

    @classmethod
    def poll(cls, context):
        mode = context.mode 
        eo = context.edit_object 
        return eo and eo.type == "MESH" and "EDIT" in mode
    
    def invoke(self, context, event):
        self.select_non_boundary = False
        if event.alt:
            self.select_non_boundary = True
        return self.execute(context)

    def execute(self, context):
        if not self.select_non_boundary:
            bpy.ops.mesh.region_to_loop()
        else:
            select_non_boundary(context)
        return {"FINISHED"}
