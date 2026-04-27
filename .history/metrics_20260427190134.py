import networkx as nx

def calculate_metrics(G):
    degree = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G)
    closeness = nx.closeness_centrality(G)
    pagerank = nx.pagerank(G)
    clustering = nx.clustering(G)
    all_metrics={}


    for node in G.nodes():
        all_metrics[node]={
            "Degree":degree[node],
            "Betweenness":betweenness[node],
            "Closeness":closeness[node],
            "Pagerank":pagerank[node],
            "Clustering":clustering[node]
        }

    if nx.is_connected(G.to_undirected()):
        avg_path=nx.average_shortest_path_length(G)
        

