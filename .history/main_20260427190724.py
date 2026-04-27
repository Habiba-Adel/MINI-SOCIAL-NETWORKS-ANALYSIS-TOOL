from graph_loader import build_graph
from metrics import calculate_metrics


G = build_graph("data/nodes.csv", "data/edges.csv", directed=True)

print("This is the nodes.csv file data: ")
print(G.nodes(data=True))

print("This is the edges.csv file data: ")
print(G.edges(data=True))