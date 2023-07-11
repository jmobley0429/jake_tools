# class SubDAndReprojectToActive(CustomOperator):

#     def __init__(self, context, args, op):
#         self._set_args(args)
#         self.context = context 
#         self.operator = op

#     def main(self):



# class OBJECT_OT_subd_and_reproject_to_active(Operator):
#     bl_idname = "object.subd_and_reproject_to_active"
#     bl_label = "SubD and Reproject"
#     bl_description = "Adds MultiRes, subdivides and Shrinkwraps object to active."
#     bl_options = {'REGISTER', "UNDO"}

#     subd_number: bpy.props.IntProperty(name="Number of Subdivisions", default=2, min=0, max=3)


#     @classmethod
#     def poll(cls, context):
#         return context.active_object is not None and len(context.selected_objects) > 1

#     def execute(self, context):
        
#         return {"FINISHED"}