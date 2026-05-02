import networkx as nx
from networkx.algorithms.community import girvan_newman, modularity
import community as community_louvain

# -----------------------------
# Girvan-Newman
# -----------------------------

def detect_communities_girvan_newman(G, max_search_level=10):

    # If there are no edges or the graph has only one node, we can consider all nodes as one community
    if G.number_of_edges() == 0 or G.number_of_nodes() <= 1:
        return [list(G.nodes())]

    comp_generator = girvan_newman(G)

    best_mod = -1.0
    best_communities = None

    # We iterate up to max_search_level to find the best level result
    for _ in range(max_search_level):
        try:
            current_communities = next(comp_generator)
        except StopIteration:
            break
        

        # Skip trivial single-node-per-community partitions on early iterations
        if len(current_communities) == G.number_of_nodes():
            break

        try:
            current_mod = modularity(G, current_communities)
            if current_mod > best_mod:
                best_mod = current_mod
                best_communities = current_communities
        except Exception:
            continue

    if best_communities is None:
        best_communities = [set(G.nodes())]

    result = [sorted(list(c)) for c in best_communities]
    result.sort(key=lambda x: x[0])
    return result


# -----------------------------
# Louvain
# -----------------------------
def detect_communities_louvain(G):

    # If there are no nodes, return empty communities and mapping
    if G.number_of_nodes() == 0:
        return [], {}

    # Louvain works on undirected graphs, so we convert if necessary
    # Because Louvain focus on connections rather than direction, we can safely ignore edge directions for community detection
    if G.is_directed():
        G = G.to_undirected()

    # This returns a dictionary where keys are node and values are community IDs
    # Like: {node: community_id}
    partition = community_louvain.best_partition(G)

    communities_dict = {}

    for node, comm_id in partition.items():
        # If this community ID hasn't been seen before, initialize a new list for it
        if comm_id not in communities_dict:
            communities_dict[comm_id] = []
        # If the community exists append the node to its community
        communities_dict[comm_id].append(node)

    communities = []

    # Return the communities as a list sorted by the first node in each community for consistent output as girvan newman
    for comm in communities_dict.values():
        communities.append(sorted(comm))

    communities.sort(key=lambda x: x[0])
    # communities : [[1,2], [3,4]]
    # partition : {1:0, 2:0, 3:1, 4:1}
    return communities, partition


# -------------------------------------------------------------------------------------------------
# Functions for displaying each node with its community assignment.
# -------------------------------------------------------------------------------------------------

# -----------------------------
# Assign each node to a community for Girvan-Newman
# -----------------------------
def assign_communities(G, communities, attr_name):
    # node → community_id
    mapping = {}

    # Assign community ID to each node based on the communities list
    for i, comm in enumerate(communities):
        for node in comm:
            mapping[node] = i

    nx.set_node_attributes(G, mapping, attr_name)

    return mapping


# -----------------------------
# Assign Louvain communities to node attributes also
# -----------------------------
def assign_louvain(G, partition):
    nx.set_node_attributes(G, partition, "louvain_community")


# -----------------------------
# Run All community detection algorithms and return results in a structured format
# -----------------------------
def run_community_detection(G, max_search_level=10):

    results = {}
    eval_graph = G.to_undirected() if G.is_directed() else G
    
    # Girvan-Newman
    gn_comms = detect_communities_girvan_newman(
        eval_graph, max_search_level=max_search_level)
    gn_map = assign_communities(eval_graph, gn_comms, "gn_community")

    results["girvan_newman"] = {
        "communities": gn_comms,
        "mapping": gn_map
    }

    # Louvain
    lv_comms, lv_partition = detect_communities_louvain(eval_graph)
    assign_louvain(eval_graph, lv_partition)

    results["louvain"] = {
        "communities": lv_comms,
        "mapping": lv_partition
    }

    return results
