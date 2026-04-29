import networkx as nx
from networkx.algorithms import community
from sklearn.metrics import normalized_mutual_info_score

def calculate_avg_conductance(graph, communities):
    if not communities:
        return 0
    conductance_values = []

    for community in communities:
        c = nx.conductance(graph, community)
        conductance_values.append(c)
    return sum(conductance_values) / len(conductance_values)

# to convert list of sets to list of labels
def to_labels(graph, communities):
    """
    Converts a list of sets (communities) into an ordered list of labels.
    Ensures the labels are aligned with the order of nodes in the graph.
    """
    labels = {}
    # enumerate gives us a unique ID (0, 1, 2...) for each community set
    for id, community in enumerate(communities):
        for node in community:
            labels[node] = id

    return [labels[node] for node in graph.nodes()]

def evaluation(graph, communities, label_name=None):
    results = {
        "Modularity": community.modularity(graph, communities),
        "Average Conductance": calculate_avg_conductance(graph, communities),
        "Number of Communities": len(communities)
    }

    if label_name:
        labels = nx.get_node_attributes(graph, label_name)
        if labels:
            true_labels = [labels[node] for node in graph.nodes()]
            detected_labels = to_labels(graph, communities)
            results["NMI"] = normalized_mutual_info_score(true_labels, detected_labels)
        else:
            results["NMI"] = "Attribute not found"
    
    return results