import networkx as nx

def calculate_metrics(G):
    degree = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G)
    closeness = nx.closeness_centrality(G)
    pagerank = nx.pagerank(G)
    clustering = nx.clustering(G)
    all_metrics={}


    for node in G.nodes():
        
