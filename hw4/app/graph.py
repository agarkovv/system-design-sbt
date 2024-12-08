from collections import deque
from typing import Any, Dict, List, Optional, Set


class Graph:
    """A directed graph implementation with basic graph operations."""

    def __init__(self):
        """Initialize an empty graph."""
        self._vertices: Dict[Any, Set[Any]] = {}
        self._weights: Dict[tuple, float] = {}

    def add_vertex(self, vertex: Any) -> None:
        """Add a vertex to the graph."""
        if vertex not in self._vertices:
            self._vertices[vertex] = set()

    def add_edge(self, from_vertex: Any, to_vertex: Any, weight: float = 1.0) -> None:
        """Add a directed edge from one vertex to another with an optional weight."""
        self.add_vertex(from_vertex)
        self.add_vertex(to_vertex)
        self._vertices[from_vertex].add(to_vertex)
        self._weights[(from_vertex, to_vertex)] = weight

    def remove_edge(self, from_vertex: Any, to_vertex: Any) -> None:
        """Remove an edge from the graph."""
        if from_vertex in self._vertices:
            self._vertices[from_vertex].discard(to_vertex)
            self._weights.pop((from_vertex, to_vertex), None)

    def get_vertices(self) -> List[Any]:
        """Return all vertices in the graph."""
        return list(self._vertices.keys())

    def get_edges(self) -> List[tuple]:
        """Return all edges in the graph as (from_vertex, to_vertex, weight) tuples."""
        return [
            (from_v, to_v, self._weights[(from_v, to_v)])
            for from_v in self._vertices
            for to_v in self._vertices[from_v]
        ]

    def get_neighbors(self, vertex: Any) -> Set[Any]:
        """Get all vertices that are connected to the given vertex."""
        return self._vertices.get(vertex, set())

    def get_weight(self, from_vertex: Any, to_vertex: Any) -> Optional[float]:
        """Get the weight of an edge between two vertices."""
        return self._weights.get((from_vertex, to_vertex))

    def has_path(self, start: Any, end: Any) -> bool:
        """Check if there is a path between start and end vertices using BFS."""
        if start not in self._vertices or end not in self._vertices:
            return False

        visited = set()
        queue = deque([start])

        while queue:
            vertex = queue.popleft()
            if vertex == end:
                return True

            if vertex not in visited:
                visited.add(vertex)
                queue.extend(self._vertices[vertex] - visited)

        return False

    def find_path(self, start: Any, end: Any) -> List[Any]:
        """Find a path between start and end vertices using BFS."""
        if start not in self._vertices or end not in self._vertices:
            return []

        visited = {start: None}
        queue = deque([start])

        while queue:
            vertex = queue.popleft()
            if vertex == end:
                path = []
                while vertex is not None:
                    path.append(vertex)
                    vertex = visited[vertex]
                return list(reversed(path))

            for next_vertex in self._vertices[vertex]:
                if next_vertex not in visited:
                    visited[next_vertex] = vertex
                    queue.append(next_vertex)

        return []

    def is_cyclic(self) -> bool:
        """Check if the graph contains any cycles using DFS."""
        visited = set()
        rec_stack = set()

        def is_cyclic_util(vertex):
            visited.add(vertex)
            rec_stack.add(vertex)

            for neighbor in self._vertices[vertex]:
                if neighbor not in visited:
                    if is_cyclic_util(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(vertex)
            return False

        for vertex in self._vertices:
            if vertex not in visited:
                if is_cyclic_util(vertex):
                    return True
        return False
