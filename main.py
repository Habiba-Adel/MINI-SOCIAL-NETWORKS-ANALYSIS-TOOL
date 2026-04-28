from graph_loader import build_graph
from metrics import calculate_metrics
from visualization import (draw_basic_graph, draw_graph_with_metrics, draw_communities, draw_advanced)
from community_detection import run_community_detection
from filtering import filter_by_centrality, filter_by_community

def main():
    print("--- Loading Data ---")
    try:
        G = build_graph("data/nodes.csv", "data/edges.csv", directed=False)
        print(f"✅ Graph loaded successfully with {G.number_of_nodes()} nodes.")
    except Exception as e:
        print(f"❌ Error loading graph: {e}")
        return

    # 2. حساب مقاييس المركزية
    metrics, avg_path = calculate_metrics(G)
    print(f"✅ Metrics calculated. Average Path Length: {avg_path}")

    print("\n" + "="*50)
    print("     MEMBER 6: INTERACTIVE NETWORK FILTERING")
    print("="*50)
    print("Choose filtering method:")
    print("1. Degree Centrality Range")
    print("2. Betweenness Centrality Range")
    print("3. Closeness Centrality Range")
    print("4. Filter by Community (Louvain)")
    print("5. Exit")

    choice = input("\nEnter your choice (1-5): ")

    if choice in ["1", "2", "3"]:
        measures_map = {"1": "Degree", "2": "Betweenness", "3": "Closeness"}
        measure_name = measures_map[choice]
        print(f"\n--- Filtering by {measure_name} Range ---")
        
        try:
            low = float(input("Enter minimum threshold (e.g., 0.1): "))
            high = float(input("Enter maximum threshold (e.g., 1.0): "))
            
            filtered_G = filter_by_centrality(G, metrics, measure_name, low, high)
            print(f"✅ Found {filtered_G.number_of_nodes()} nodes.")
            
            if filtered_G.number_of_nodes() > 0:
                if input("Show visual for filtered graph? (y/n): ").lower() == 'y':
                    draw_basic_graph(filtered_G, layout_type="spring")
        except ValueError:
            print("❌ Error: Please enter numeric values.")

    elif choice == "4":
        print("\n--- Filtering by Community ---")
        run_community_detection(G) 
        
        try:
            comm_id = int(input("Enter community ID (e.g., 0, 1): "))
            filtered_G = filter_by_community(G, "louvain_community", comm_id)
            
            print(f"✅ Found {filtered_G.number_of_nodes()} nodes in Community {comm_id}.")
            if filtered_G.number_of_nodes() > 0:
                if input("Show visual? (y/n): ").lower() == 'y':
                    draw_basic_graph(filtered_G, layout_type="spring")
        except ValueError:
            print("❌ Error: Please enter a valid community ID.")

    elif choice == "5":
        print("Exiting...")

if __name__ == "__main__":
    main()