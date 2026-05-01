import networkx as nx

def filter_by_centrality (G, metrics, measure, min, max):
    filtered_nodes= []

    for node, node_data in metrics.items():
        if measure in node_data:
            val = node_data[measure]
            if min <= val <= max:
                filtered_nodes.append(node)

    return G.subgraph(filtered_nodes)


def filter_by_community (G, community_attribute, target_community):
    filtered_nodes=[]

    for node, data in G.nodes(data=True):
        if data.get(community_attribute) == target_community:
            filtered_nodes.append(node)
            
    return G.subgraph(filtered_nodes)
