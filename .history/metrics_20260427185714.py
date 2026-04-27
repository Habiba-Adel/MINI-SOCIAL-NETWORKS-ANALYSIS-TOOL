import networkx as nx

def calculate_metrics(G):
    degree=nx.degree_centrality(G)