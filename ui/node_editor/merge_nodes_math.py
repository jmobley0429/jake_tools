import pprint
import bpy
from bpy import data as D
from bpy import context as C
from bpy.types import Menu
from mathutils import Vector
import numpy as np
import string

SPACING_MULT = 1.4

MATH_OPS = [
    "ADD",
    "SUBTRACT",
    "MULTIPLY",
    "DIVIDE",
    "LESS_THAN",
    "GREATER_THAN",
    "POWER",
    "MODULO",
]

VEC_MATH_OPS = [
    "ADD",
    "SUBTRACT",
    "MULTIPLY",
    "DIVIDE",
    "NORMALIZE",
    "LENGTH",
    "DISTANCE",
    "SCALE",
]


class SelectedNodes:

    def __init__(self, node_tree, use_vector=False):
        self.node_tree = node_tree
        self.sel_nodes = self.get_selected_nodes()
        self.selection_has_vector = use_vector
        if self.sel_nodes:
            self._get_nodes_data()

    def __len__(self):
        return len(self.sel_nodes)

    @property
    def none_selected(self):
        return len(self.sel_nodes) == 0

    def get_selected_nodes(self):
        return sorted(
            [node for node in self.node_tree.nodes if node.select],
            key=lambda node: node.location.y,
            reverse=True,
        )

    @staticmethod
    def node_has_vector(node):
        return node.outputs[0].type == "VECTOR"

    def get_max_node_width(sel_nodes):
        return max([node.width for node in sel_nodes])

    @property
    def math_node_type(self):
        if self.selection_has_vector:
            return "ShaderNodeVectorMath"
        return "ShaderNodeMath"

    def get_first_output(self, node):
        for output in node.outputs:
            if output.type in ["VALUE", "VECTOR", "RGBA"]:
                return output

    def _get_nodes_data(self):
        self.has_vectors = []
        self.widths = []
        self.locs = []
        for node in self.sel_nodes:
            self.has_vectors.append(self.node_has_vector(node))
            self.widths.append(node.width)
            self.locs.append(get_node_bbox_center(node))
        self.selection_has_vector = any(self.has_vectors)
        self.average_loc = np.mean(self.locs, axis=0)
        self.max_width = max(self.widths)

    @property
    def width_with_mult(self):
        return self.max_width * SPACING_MULT

    @property
    def new_node_loc(self):
        new_node_loc = Vector(self.average_loc)
        new_node_loc.x += self.width_with_mult
        return new_node_loc

    def pair_node_inputs_and_outputs(self, math_node):
        outs = []
        ins = math_node.inputs[:]

        for i, node in enumerate(self.sel_nodes):
            if i < len(ins):
                outs.append(self.get_first_output(node))

        if math_node.operation == "SCALE":
            outs.sort(key=lambda out: out.type, reverse=True)
            ins = ins[:: len(ins) - 1]

        return zip(outs, ins)


def get_node_screen():
    for area in C.screen.areas[:]:
        if area.type == "NODE_EDITOR":
            for space in area.spaces[:]:
                if space.type == "NODE_EDITOR":
                    return space.node_tree


def get_node_tree_from_context(context):
    for space in context.area.spaces[:]:
        if space.type == "NODE_EDITOR":
            return space.node_tree


def set_node_positions(mouse_loc, nodes):
    loc = mouse_loc
    offset = nodes[0].width * 1.1
    for node in nodes:
        node.location = loc
        loc.x += offset
    align_nodes_on_center(nodes)


def get_node_bbox_center(node):
    x, y = node.width, node.height
    loc = node.location
    bbox_center = node.location.x + x / 2, node.location.y + y / 2
    return Vector(bbox_center)


def align_nodes_on_center(nodes):
    max_y = np.max([node.location.y + node.height for node in nodes])
    min_y = np.min([node.location.y for node in nodes])
    mean_y_pos = (min_y + max_y) / 2
    for node in nodes:
        node_center = Vector(
            bpy.context.region.view2d.view_to_region(*get_node_bbox_center(node))
        )
        node.location.y = mean_y_pos + node_center.y


# def add_capture_attr_nodes(node_tree, mouse_loc, attr_to_capture, domain):
#     types = [
#         "GeometryNodeInputPosition",
#         "GeometryNodeCaptureAttribute",
#     ]
#     new_nodes = [node_tree.nodes.new(_type) for _type in types]
#     field_node, capture_node = new_nodes
#     capture_node.data_type = "FLOAT_VECTOR"
#     capture_node.domain = domain
#     node_tree.links.new(field_node.outputs[0], capture_node.inputs[1])
#     set_node_positions(Vector(mouse_loc), new_nodes)


def get_current_mouse_coords(context, event):
    region_locs = event.mouse_region_x, event.mouse_region_y
    return context.region.view2d.region_to_view(*region_locs)


def get_nice_str(bad_str):
    return string.capwords(bad_str.replace("_", " "))


def get_math_operators(context):
    tree = get_node_tree_from_context(context)
    nodes_obj = SelectedNodes(tree)
    hv = nodes_obj.selection_has_vector
    if hv:
        return VEC_MATH_OPS
    return MATH_OPS


def get_math_operation_items(self, context):
    math_ops = get_math_operators(context)
    items = []
    for op in math_ops:
        enum_item = []
        for i in range(3):
            if i == 2:
                enum_item.append(get_nice_str(op))
            else:
                enum_item.append(op)
        items.append(tuple(enum_item))
    return items


def main(context, op):
    tree = get_node_tree_from_context(context)
    nodes_obj = SelectedNodes(tree, use_vector=op.use_vector)
    operation = op.math_operation
    node_type = nodes_obj.math_node_type
    if nodes_obj.none_selected:
        new_node_loc = op.mouse_loc
        math_node = add_new_node(tree, operation, new_node_loc, node_type)

    else:
        new_node_loc = nodes_obj.new_node_loc
        math_node = add_new_node(tree, operation, new_node_loc, node_type)
        ins_outs = nodes_obj.pair_node_inputs_and_outputs(math_node)
        for inp, out in ins_outs:
            tree.links.new(out, inp)
    return {"FINISHED"}


def add_new_node(tree, operation, new_node_loc, node_type):
    math_node = tree.nodes.new(type=node_type)
    math_node.operation = operation
    math_node.location = new_node_loc
    return math_node


class NODE_OT_add_math_operation_nodes(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "node.add_math_operation_nodes"
    bl_label = "Add Math Node"
    bl_options = {"REGISTER", "UNDO"}

    math_operation: bpy.props.EnumProperty(
        items=get_math_operation_items,
        name="Math Operation",
        # set=get_math_operation_items,
    )

    @classmethod
    def poll(cls, context):
        return context.area.type == "NODE_EDITOR"

    def invoke(self, context, event):
        if event.alt:
            self.use_vector = True
        else:
            self.use_vector = False
        self.mouse_loc = get_current_mouse_coords(context, event)
        return self.execute(context)

    def execute(self, context):
        return main(context, self)


class PIE_MT_merge_nodes_math(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "Math Node Pie"
    bl_idname = "PIE_MT_merge_nodes_math"

    def draw(self, context):
        ops = get_math_operators(context)

        layout = self.layout

        pie = layout.menu_pie()

        merge_nodes_op = NODE_OT_add_math_operation_nodes.bl_idname
        for operation in ops:
            label = get_nice_str(operation)
            op = pie.operator(merge_nodes_op, text=label)
            op.math_operation = operation


kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Node Editor",
        "letter": "E",
        "shift": 1,
        "ctrl": 0,
        "alt": 0,
        "space_type": "NODE_EDITOR",
        "region_type": "WINDOW",
        "keywords": {"name": PIE_MT_merge_nodes_math.bl_idname},
    }
]
