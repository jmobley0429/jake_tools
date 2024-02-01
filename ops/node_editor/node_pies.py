# import bpy
# from bpy import data as D
# from bpy import context as C
# from mathutils import Vector
# import numpy as np


# def get_node_screen():
#     for area in C.screen.areas[:]:
#         if area.type == "NODE_EDITOR":
#             for space in area.spaces[:]:
#                 if space.type == "NODE_EDITOR":
#                     return space.node_tree


# def get_node_tree_from_context(context):
#     for space in context.area.spaces[:]:
#         if space.type == "NODE_EDITOR":
#             return space.node_tree


# def set_node_positions(mouse_loc, nodes):
#     loc = mouse_loc
#     offset = nodes[0].width * 1.1
#     for node in nodes:
#         node.location = loc
#         loc.x += offset
#     align_nodes_on_center(nodes)


# def get_node_bbox_center(node):
#     x, y = node.width, node.height
#     loc = node.location
#     bbox_center = node.location.x + x / 2, node.location.y + y / 2
#     return Vector(bbox_center)


# def align_nodes_on_center(nodes):
#     max_y = np.max([node.location.y + node.height for node in nodes])
#     min_y = np.min([node.location.y for node in nodes])
#     mean_y_pos = (min_y + max_y) / 2
#     for node in nodes:
#         node_center = Vector(
#             bpy.context.region.view2d.view_to_region(*get_node_bbox_center(node))
#         )
#         node.location.y = mean_y_pos + node_center.y


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


# def get_current_mouse_coords(context, event):
#     region_locs = event.mouse_region_x, event.mouse_region_y
#     return context.region.view2d.region_to_view(*region_locs)


# class NODE_OT_add_custom_node(bpy.types.Operator):
#     """Tooltip"""

#     bl_idname = "node.add_custom_node"
#     bl_label = "Add Custom Node"
#     bl_options = {"REGISTER", "UNDO"}

#     node_type: bpy.props.StringProperty(name="Node Type")

#     @classmethod
#     def poll(cls, context):
#         return context.area.type == "NODE_EDITOR"

#     def invoke(self, context, event):
#         self.mouse_loc = get_current_mouse_coords(context, event)
#         return self.execute(context)

#     def execute(self, context):
#         node_tree = get_node_tree_from_context(context)
#         #        new_node = node_tree.nodes.new('ShaderNodeMath')
#         #        new_node.location = self.mouse_loc
#         #        new_node.operation = "MULTIPLY"
#         add_capture_attr_nodes(
#             node_tree, self.mouse_loc, "GeometryNodeInputPosition", "POINT"
#         )

#         return {"FINISHED"}
