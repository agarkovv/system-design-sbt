import allure
import pytest
from app.graph import Graph
from app.main import main, print_menu


@allure.epic("Graph Operations")
class TestGraph:

    @pytest.fixture
    def graph(self):
        return Graph()

    @allure.feature("Basic Operations")
    @allure.story("Vertex Management")
    def test_add_vertex(self, graph):
        with allure.step("Add vertex 'A'"):
            graph.add_vertex("A")
            assert "A" in graph.get_vertices()

    @allure.feature("Basic Operations")
    @allure.story("Edge Management")
    def test_add_edge(self, graph):
        with allure.step("Add edge from 'A' to 'B'"):
            graph.add_edge("A", "B", 2.0)
            assert "B" in graph.get_neighbors("A")
            assert graph.get_weight("A", "B") == 2.0

    @allure.feature("Basic Operations")
    @allure.story("Edge Management")
    def test_remove_edge(self, graph):
        with allure.step("Add and remove edge"):
            graph.add_edge("A", "B")
            graph.remove_edge("A", "B")
            assert "B" not in graph.get_neighbors("A")

    @allure.feature("Path Finding")
    @allure.story("Path Existence")
    def test_has_path(self, graph):
        with allure.step("Create path A->B->C"):
            graph.add_edge("A", "B")
            graph.add_edge("B", "C")

        with allure.step("Check path existence"):
            assert graph.has_path("A", "C")
            assert not graph.has_path("C", "A")

    @allure.feature("Path Finding")
    @allure.story("Path Finding")
    def test_find_path(self, graph):
        with allure.step("Create path A->B->C"):
            graph.add_edge("A", "B")
            graph.add_edge("B", "C")

        with allure.step("Find path from A to C"):
            path = graph.find_path("A", "C")
            assert path == ["A", "B", "C"]

    @allure.feature("Graph Analysis")
    @allure.story("Cycle Detection")
    def test_is_cyclic(self, graph):
        with allure.step("Create acyclic graph"):
            graph.add_edge("A", "B")
            graph.add_edge("B", "C")
            assert not graph.is_cyclic()

        with allure.step("Add cycle"):
            graph.add_edge("C", "A")
            assert graph.is_cyclic()

    @allure.feature("Error Handling")
    @allure.story("Invalid Operations")
    def test_invalid_operations(self, graph):
        with allure.step("Try to find path with non-existent vertices"):
            assert not graph.has_path("X", "Y")
            assert graph.find_path("X", "Y") == []

        with allure.step("Try to get weight of non-existent edge"):
            assert graph.get_weight("X", "Y") is None

    @allure.feature("Basic Operations")
    @allure.story("Vertex Management")
    def test_add_existing_vertex(self, graph):
        """Test adding the same vertex multiple times"""
        with allure.step("Add vertex 'A' twice"):
            graph.add_vertex("A")
            graph.add_vertex("A")  # Should not raise error
            assert len(graph.get_vertices()) == 1

    @allure.feature("Basic Operations")
    @allure.story("Edge Management")
    def test_remove_nonexistent_edge(self, graph):
        """Test removing an edge that doesn't exist"""
        with allure.step("Remove edge from non-existent vertex"):
            graph.remove_edge("X", "Y")  # Should not raise error
            assert "X" not in graph.get_vertices()

    @allure.feature("Basic Operations")
    @allure.story("Edge Management")
    def test_get_neighbors_nonexistent_vertex(self, graph):
        """Test getting neighbors of non-existent vertex"""
        with allure.step("Get neighbors of non-existent vertex"):
            neighbors = graph.get_neighbors("X")
            assert neighbors == set()

    @allure.feature("Graph Analysis")
    @allure.story("Cycle Detection")
    def test_is_cyclic_empty_graph(self, graph):
        """Test cycle detection on empty graph"""
        with allure.step("Check empty graph for cycles"):
            assert not graph.is_cyclic()

    @allure.feature("Graph Analysis")
    @allure.story("Cycle Detection")
    def test_is_cyclic_single_vertex(self, graph):
        """Test cycle detection with single vertex"""
        with allure.step("Add single vertex and check for cycles"):
            graph.add_vertex("A")
            assert not graph.is_cyclic()

    @allure.feature("Path Finding")
    @allure.story("Path Finding")
    def test_find_path_to_self(self, graph):
        """Test finding path from vertex to itself"""
        with allure.step("Add vertex and find path to itself"):
            graph.add_vertex("A")
            path = graph.find_path("A", "A")
            assert path == ["A"]

    @allure.feature("Path Finding")
    @allure.story("Path Finding")
    def test_find_path_disconnected(self, graph):
        """Test finding path between disconnected vertices"""
        with allure.step("Add disconnected vertices"):
            graph.add_vertex("A")
            graph.add_vertex("B")
            path = graph.find_path("A", "B")
            assert path == []

    @allure.feature("Graph Operations")
    @allure.story("Menu Functions")
    def test_print_menu(self, capsys):
        """Test menu printing functionality"""
        with allure.step("Print menu"):
            print_menu()
            captured = capsys.readouterr()
            assert "Graph Operations:" in captured.out
            assert "1. Add vertex" in captured.out
            assert "0. Exit" in captured.out

    @allure.feature("Graph Operations")
    @allure.story("Main Function")
    def test_main_function(self, capsys):
        """Test main function execution"""
        with allure.step("Run main function"):
            main()
            captured = capsys.readouterr()
            assert "Running demo graph operations..." in captured.out
            assert "Creating vertices A, B, C..." in captured.out
            assert "Demo completed. Exiting..." in captured.out

    @allure.feature("Graph Operations")
    @allure.story("Edge Operations")
    def test_edge_operations_comprehensive(self, graph):
        """Test comprehensive edge operations"""
        with allure.step("Add multiple edges"):
            graph.add_edge("A", "B", 1.5)
            graph.add_edge("B", "C", 2.0)
            graph.add_edge("C", "D", 3.0)

        with allure.step("Verify edges"):
            edges = graph.get_edges()
            assert len(edges) == 3
            assert ("A", "B", 1.5) in edges
            assert ("B", "C", 2.0) in edges
            assert ("C", "D", 3.0) in edges

    @allure.feature("Graph Operations")
    @allure.story("Path Operations")
    def test_path_operations_comprehensive(self, graph):
        """Test comprehensive path operations"""
        with allure.step("Create complex path"):
            graph.add_edge("A", "B")
            graph.add_edge("B", "C")
            graph.add_edge("C", "D")
            graph.add_edge("B", "D")

        with allure.step("Test various paths"):
            assert graph.has_path("A", "D")
            assert graph.find_path("A", "D") == ["A", "B", "D"]
            assert not graph.has_path("D", "A")
            assert graph.find_path("D", "A") == []

    @allure.feature("Graph Operations")
    @allure.story("Cycle Detection")
    def test_cycle_detection_comprehensive(self, graph):
        """Test comprehensive cycle detection"""
        with allure.step("Create complex graph with multiple cycles"):
            graph.add_edge("A", "B")
            graph.add_edge("B", "C")
            graph.add_edge("C", "A")
            graph.add_edge("C", "D")
            graph.add_edge("D", "E")
            graph.add_edge("E", "C")

        with allure.step("Verify cycles"):
            assert graph.is_cyclic()

            # Remove cycle
            graph.remove_edge("C", "A")
            graph.remove_edge("E", "C")
            assert not graph.is_cyclic()

    @allure.feature("Graph Operations")
    @allure.story("Vertex Operations")
    def test_vertex_operations_comprehensive(self, graph):
        """Test comprehensive vertex operations"""
        with allure.step("Add and verify vertices"):
            vertices = ["A", "B", "C", "D", "E"]
            for vertex in vertices:
                graph.add_vertex(vertex)

            assert set(graph.get_vertices()) == set(vertices)

        with allure.step("Test vertex neighbors"):
            graph.add_edge("A", "B")
            graph.add_edge("A", "C")
            assert graph.get_neighbors("A") == {"B", "C"}
            assert graph.get_neighbors("B") == set()

    @allure.feature("Graph Operations")
    @allure.story("Weight Operations")
    def test_weight_operations_comprehensive(self, graph):
        """Test comprehensive weight operations"""
        with allure.step("Add edges with different weights"):
            weights = {("A", "B"): 1.5, ("B", "C"): 2.0, ("C", "D"): 3.5}
            for (from_v, to_v), weight in weights.items():
                graph.add_edge(from_v, to_v, weight)

        with allure.step("Verify weights"):
            for (from_v, to_v), weight in weights.items():
                assert graph.get_weight(from_v, to_v) == weight

    @allure.feature("Graph Operations")
    @allure.story("Error Cases")
    def test_error_cases_comprehensive(self, graph):
        """Test comprehensive error cases"""
        with allure.step("Test operations on empty graph"):
            assert graph.get_vertices() == []
            assert graph.get_edges() == []
            assert not graph.is_cyclic()
            assert graph.find_path("A", "B") == []

        with allure.step("Test invalid operations"):
            assert graph.get_weight("X", "Y") is None
            graph.remove_edge("X", "Y")  # Should not raise error
            assert graph.get_neighbors("Z") == set()

    @allure.feature("Graph Operations")
    @allure.story("Complex Graph")
    def test_complex_graph_operations(self, graph):
        """Test operations on a complex graph"""
        with allure.step("Create complex graph"):
            # Create a more complex graph structure
            edges = [
                ("A", "B", 1.0),
                ("B", "C", 2.0),
                ("C", "D", 3.0),
                ("D", "E", 4.0),
                ("B", "D", 5.0),
                ("C", "E", 6.0),
            ]
            for from_v, to_v, weight in edges:
                graph.add_edge(from_v, to_v, weight)

        with allure.step("Verify complex graph"):
            assert len(graph.get_vertices()) == 5
            assert len(graph.get_edges()) == 6
            assert graph.find_path("A", "E") in [
                ["A", "B", "D", "E"],
                ["A", "B", "C", "E"],
            ]
            assert not graph.is_cyclic()
