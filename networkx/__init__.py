class NodeView:
    def __init__(self, mapping):
        self._mapping = mapping

    def __getitem__(self, item):
        return self._mapping[item]

    def __iter__(self):
        return iter(self._mapping)

    def __call__(self, data=False):
        if data:
            return list(self._mapping.items())
        return list(self._mapping.keys())


class EdgeView:
    def __init__(self, edges):
        self._edges = edges

    def __getitem__(self, item):
        u, v = item
        return self._edges[u][v]

    def __iter__(self):
        for u, targets in self._edges.items():
            for v in targets:
                yield (u, v)

    def __call__(self, data=False):
        for u, targets in self._edges.items():
            for v, attrs in targets.items():
                yield (u, v, attrs) if data else (u, v)


class DiGraph:
    def __init__(self):
        self._nodes = {}
        self._edges = {}

    def add_node(self, node, **attrs):
        self._nodes[node] = attrs

    def add_edge(self, u, v, **attrs):
        self._edges.setdefault(u, {})[v] = attrs

    @property
    def nodes(self):
        return NodeView(self._nodes)

    @property
    def edges(self):
        return EdgeView(self._edges)
