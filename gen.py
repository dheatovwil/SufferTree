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


def dot(node, f: graphviz.Digraph, state):
    nmap = state.nmap
    if node.is_leaf:
        return

    for edge in node.table:
        if edge is None:
            continue
        if edge.dst not in nmap:
            nmap[edge.dst] = "n%d" % state.ctr
            state.ctr += 1
            f.node(nmap[edge.dst], str(edge.label))
        f.edge(nmap[edge.src], nmap[edge.dst])
        dot(edge.dst, f, state)


def dot_suf(node, f, state):
    if node.is_leaf:
        return

    nmap = state.nmap

    for edge in node.table:
        if edge is None:
            continue
        dot_suf(edge.dst, f, state)

    if node.link is not None:
        f.edge(nmap[node], nmap[node.link], _attributes=[("style", "dashed"), ("color", "red")])


@dataclass
class State:
    nmap: dict
    ctr: int = 0


def gen_dot(root):
    f = graphviz.Digraph("sfx3", format="png")

    nmap = {            # map node to a string identifier
        root: "ROOT"
    }
    s = State(nmap)

    dot(root, f, s)
    dot_suf(root, f, s)  # draw suffix link

    return f


