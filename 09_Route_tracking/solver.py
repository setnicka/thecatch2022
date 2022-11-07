#!/usr/bin/python3

import pydot

target = 163912

graphs = pydot.graph_from_dot_file("Area_52.dot")
graph: pydot.Dot = graphs[0]
dot_nodes: list[pydot.Node] = graph.get_nodes()
dot_edges: list[pydot.Edge] = graph.get_edges()


class Node:
    code: str | None
    edges: list[tuple[str, int]]
    used: bool

    def __init__(self, code: str | None):
        self.code = code.replace('"', '')
        self.edges = []
        self.used = False


nodes: dict[str, Node] = {}
for n in dot_nodes:
    attrs = n.get_attributes()
    nodes[n.get_name()] = Node(attrs['code'] if 'code' in attrs else "")

for e in dot_edges:
    s = e.get_source()
    d = e.get_destination()
    dist = int(e.get_attributes()['dist'])
    nodes[s].edges.append((d, dist))

start = '000'
end = '000'


def dfs(id: str, len: int = 0, path: str = ""):
    node = nodes[id]

    if id == end and len == target:
        print(path)
        return True

    if node.used:
        return False
    node.used = True

    path += node.code

    if len >= target:
        node.used = False
        return False
    for (n, dist) in node.edges:
        if dfs(n, len+dist, path):
            return True

    node.used = False
    return False


dfs(start)
