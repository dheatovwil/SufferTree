"""
This script generate a json file describing the graph, which will be passed to the
 renderer.

A node should implement this interface:

    .is_leaf -> bool: Indicates whether this node contains child or not
    .table -> List[Optional[Edge]]: Table that can store None or an outward Edge

An edge should implement this interface

    .label -> str: The label of the edge

Visualization Note:
    * The renderer uses node label instead of edge label, hence the edge label is
       stored as the label of target node

"""
import json


def traverse(node, obj):
    """
    Populate the `obj` with node data
    :param node: A node to start from (call with root to traverse the whole graph)
    :param obj: A list object to stores children nodes (the `json["children"]` object)
    :return: None
    """
    if node.is_leaf:
        return

    for child in node.table:
        if child is None:
            continue
        edge = child
        cl = []
        obj.append({
            "name": edge.label,
            "children": cl
        })
        traverse(edge.dst, cl)  # populate child list of each child node


def generate_json(root) -> dict:
    """
    Wrapper to traverse from root
    :param root: A node that implements the prescribed interface
    :return: JSON describing the graph
    """
    g_json = {
        "name": "root",
        "children": []
    }
    traverse(root, g_json["children"])

    return g_json


def main(root):
    """
    Simple entry point, starts here if you don't know what you're doing
    :param root: A node that implements the prescribed interface
    :return: None, write output to `tree.json` file, renderer will read that file by default.
    """
    with open("tree.json", "w") as f:
        json.dump(generate_json(root), f)
