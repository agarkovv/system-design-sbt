from app.graph import Graph


def print_menu():
    print("\nGraph Operations:")
    print("1. Add vertex")
    print("2. Add edge")
    print("3. Remove edge")
    print("4. Show vertices")
    print("5. Show edges")
    print("6. Check path existence")
    print("7. Find path")
    print("8. Check if cyclic")
    print("0. Exit")


def main(non_interactive=False):
    graph = Graph()

    # Always run in demo mode for deployment
    print("Running demo graph operations...")

    # Create a sample graph
    print("\nCreating vertices A, B, C...")
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")

    print("\nAdding edges: A->B (weight 1.0), B->C (weight 2.0)...")
    graph.add_edge("A", "B", 1.0)
    graph.add_edge("B", "C", 2.0)

    # Display graph information
    print("\nGraph structure:")
    print("Vertices:", graph.get_vertices())
    print("\nEdges:")
    for from_v, to_v, weight in graph.get_edges():
        print(f"  {from_v} -> {to_v} (weight: {weight})")

    print("\nPath analysis:")
    print("Path from A to C:", " -> ".join(graph.find_path("A", "C")))
    print("Is graph cyclic:", graph.is_cyclic())

    print("\nDemo completed. Exiting...")


if __name__ == "__main__":
    main(non_interactive=False)
