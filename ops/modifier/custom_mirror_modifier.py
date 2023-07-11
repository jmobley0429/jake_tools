#modifier
import bpy
from bpy.types import Operator
from custom_operator import *


good_obj_types = [
    'OBJECT',
    'CURVE'
]


class CustomAddMirrorModifier(CustomOperator, Operator):
    """Add Mirror Custom Modifier"""

    bl_idname = "object.custom_mirror_modifier"
    bl_label = "Add Custom Mirror"
    bl_options = {"REGISTER", "UNDO"}

    mirror_type: bpy.props.StringProperty(
        default="",
    )
    mirror_direction: bpy.props.StringProperty(
        default="",
    )
    bisect: bpy.props.BoolProperty(default=True)
    bisect_only: bpy.props.BoolProperty(default=False)

    

    def invoke(self, context, event):
        self.multi_object = False
        self.bisect_only = False
        if event.alt:
            self.bisect = False
        if event.ctrl:
            self.bisect_only = True

        return self.execute(context)

    def add_mirror_mod(self, obj):
        if self.bisect and not self.multi_object:
            self._bisect_mesh()
        if not self.bisect_only:
            bpy.ops.object.modifier_add(type='MIRROR')
            axis_index = self.mirror_axis
            mirror_mod = obj.modifiers[:][-1]
            for i in range(3):
                mirror_mod.use_axis[i] = False
                mirror_mod.use_bisect_axis[i] = False
            mirror_mod.use_axis[axis_index] = True
            mirror_mod.use_bisect_axis[axis_index] = True
            # mirror_mod.use_mirror_u = True
            mirror_mod.use_clip = True
            if self.multi_object:
                mirror_mod.mirror_object = self.mirror_obj
            if self.mirror_type not in {
                "Z_POS",
                "X_POS",
                "Y_POS",
            }:
                mirror_mod.use_bisect_flip_axis[axis_index] = True

    def execute(self, context):
        in_edit_mode = bool(bpy.context.object.mode == "EDIT")
        if in_edit_mode:
            bpy.ops.object.mode_set(mode="OBJECT")
        if len(context.selected_objects) > 1:
            self.multi_object = True
            objs = set([obj for obj in context.selected_objects if obj.data is not None])
            mirror_obj = set([context.active_object])
            objs = objs - mirror_obj
            self.mirror_obj = self.get_active_obj()
            for obj in objs:
                context.view_layer.objects.active = obj
                self.add_mirror_mod(obj)
        else:
            obj = self.get_active_obj()
            self.add_mirror_mod(obj)
        if in_edit_mode:
            bpy.ops.object.mode_set(mode="EDIT")
        return {'FINISHED'}

    def _bisect_mesh(self):
        C = bpy.context
        obj = C.active_object
        bm = bmesh.new()
        me = obj.data
        bm.from_mesh(me)

        def get_geom(bm):
            geom = []
            geom.extend(bm.verts[:])
            geom.extend(bm.edges[:])
            geom.extend(bm.faces[:])
            return geom

        kwargs = self.bisect_args

        ret = bmesh.ops.bisect_plane(
            bm,
            geom=get_geom(bm),
            dist=0.0001,
            plane_co=(0, 0, 0),
            **kwargs,
        )

        bm.to_mesh(me)
        me.update()

    @property
    def mirror_axis(self):
        if self.mirror_type:
            if "X" in self.mirror_type:
                return 0
            elif "Y" in self.mirror_type:
                return 1
            return 2

    @property
    def bisect_args(self):
        if self.mirror_type:
            vals = {
                'X_NEG': {
                    'plane_no': (1, 0, 0),
                    'clear_inner': False,
                    'clear_outer': True,
                },
                'Y_NEG': {
                    'plane_no': (0, 1, 0),
                    'clear_inner': False,
                    'clear_outer': True,
                },
                'Z_NEG': {
                    'plane_no': (0, 0, 1),
                    'clear_inner': False,
                    'clear_outer': True,
                },
                'X_POS': {
                    'plane_no': (1, 0, 0),
                    'clear_inner': True,
                    'clear_outer': False,
                },
                'Y_POS': {
                    'plane_no': (0, 1, 0),
                    'clear_inner': True,
                    'clear_outer': False,
                },
                'Z_POS': {
                    'plane_no': (0, 0, 1),
                    'clear_inner': True,
                    'clear_outer': False,
                },
            }

            return vals[self.mirror_type]