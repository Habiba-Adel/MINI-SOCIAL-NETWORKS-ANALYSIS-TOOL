import networkx as nx
from networkx.algorithms.community import girvan_newman
import community as community_louvain


# -----------------------------
# Girvan-Newman
# -----------------------------
def detect_communities_girvan_newman(G, level=1):

    # If there are no edges or the graph has only one node, we can consider all nodes as one community
    if G.number_of_edges() == 0 or G.number_of_nodes() <= 1:
        return [list(G.nodes())]

    comp = girvan_newman(G)
    # First all nodes are in one community, then it splits into 2, then 3, etc. We want to get the communities at the specified level.
    communities = [set(G.nodes())]

    for _ in range(level):
        try:
            communities = next(comp)
        except StopIteration:
            break

    # Convert from sets to lists for and save in a sorted community list
    result = []
    for c in communities:
        result.append(sorted(list(c)))

    # sort results by the first node in each community for consistent output
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
# These Functions are not necessary but it's for displaying each node with its community assignment.
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
def run_community_detection(G, level=1):

    results = {}

    # Girvan-Newman
    gn_comms = detect_communities_girvan_newman(G, level=level)
    gn_map = assign_communities(G, gn_comms, "gn_community")

    results["girvan_newman"] = {
        "communities": gn_comms,
        "mapping": gn_map
    }

    # Louvain
    lv_comms, lv_partition = detect_communities_louvain(G)
    assign_louvain(G, lv_partition)

    results["louvain"] = {
        "communities": lv_comms,
        "mapping": lv_partition
    }

    return results
