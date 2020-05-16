"""
A node should implement this interface:

    .is_leaf -> bool: Indicates whether this node contains child or not
    .table -> List[Optional[Edge]]: Table that can store None or an outward Edge
    .link -> The suffix link pointer

An edge should implement this interface

    .label -> str: The label of the edge

Visualization Note:
    * The label is put at the node instead of on the edge.

"""
import graphviz
from dataclasses import dataclass


def traverse(node, edge_handler=lambda x: None, node_handler=lambda x: None):
    if node.is_leaf:
        return

    for edge in node.table:
        if edge is None:
            continue
        edge_handler(edge)
        traverse(edge.dst, edge_handler, node_handler)

    node_handler(node)


def dot(node, f: graphviz.Digraph, state):
    nmap = state.nmap

    def edge_handler(edge):
        if edge.dst not in nmap:
            nmap[edge.dst] = "n%d" % state.ctr
            state.ctr += 1
            f.node(nmap[edge.dst], str(edge.label))
        f.edge(nmap[edge.src], nmap[edge.dst])

    traverse(node, edge_handler=edge_handler)


def dot_suf(node, f, state):
    nmap = state.nmap

    def node_handler(node):
        if node.link is not None:
            f.edge(nmap[node], nmap[node.link], _attributes=[("style", "dashed"), ("color", "red")])

    traverse(node, node_handler=node_handler)


def dot_inc(node, f: graphviz.Digraph, state, higher):
    nmap = state.nmap
    created = higher["created"]

    def edge_handler(edge):
        if edge.dst not in nmap:
            nmap[edge.dst] = "n%d" % state.ctr
            state.ctr += 1
            attr = []
            if edge.dst not in created:
                attr = [("fillcolor", "yellow"), ("style", "filled")]
                created.append(edge.dst)
            f.node(nmap[edge.dst], str(edge.label), _attributes=attr)
        f.edge(nmap[edge.src], nmap[edge.dst])

    traverse(node, edge_handler=edge_handler)


@dataclass
class State:
    nmap: dict
    ctr: int = 0


def gen_dot(root, higher=None, attr=None):
    f = graphviz.Digraph("sfx3", format="png", graph_attr=attr)

    nmap = {            # map node to a string identifier
        root: "ROOT"
    }
    s = State(nmap)

    if higher:
        dot_inc(root, f, s, higher)
    else:
        dot(root, f, s)
    dot_suf(root, f, s)  # draw suffix link

    return f


