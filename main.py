from graph_loader import build_graph
from metrics import calculate_metrics

from visualization import (draw_basic_graph, draw_graph_with_metrics , draw_communities,draw_advanced)


G = build_graph("data/nodes.csv", "data/edges.csv", directed=True)

print("This is the nodes.csv file data: ")
print(G.nodes(data=True))

print("This is the edges.csv file data: ")
print(G.edges(data=True))


metrics , avg_path =calculate_metrics(G)
print("Graph Metrics:")
for node , values in metrics.items():
    print(node , values)

print ("Average Path Length:" , avg_path)    


print("\n===== VISUALIZATION TEST =====")

print("""
===== Choose Graph Layout =====
1. Spring (Force Directed)
2. Circular
3. Hierarchical
==============================
""")

choice = input("Enter your choice (1/2/3): ")

layouts = {
    "1": "spring",
    "2": "circular",
    "3": "hierarchical"
}

layout = layouts.get(choice, "spring")

print(f"\n✅ You selected: {layout}")
draw_basic_graph(G, layout)
draw_graph_with_metrics(G, layout)
draw_communities(G, layout)
draw_advanced(G, layout)