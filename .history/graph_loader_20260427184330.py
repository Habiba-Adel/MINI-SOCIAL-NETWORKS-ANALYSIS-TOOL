import pandas as pd
import networkx as nx
import os


# then now we will define the function that will build the graph to make it reusable and can be used easily
# i will make it default as it is undirected until i get in the third parameter that the graph will be directed and getting true
def build_graph(nodes_path,edges_path,node_id_col='id',source_col='source',target_col='target',directed=False):   
    # now the first main step is to build the graph using this csv files but we need to
    # make validation first to check if this files already existed or no

    if not os.path.exists(nodes_path):
        raise FileNotFoundError(f"Nodes file not found: {nodes_path}")

    if not os.path.exists(edges_path):
        raise FileNotFoundError(f"Edges file not found: {edges_path}")
    
    # now we ensure that the files existed so now we need to load the data 
    nodes_df = pd.read_csv(nodes_path)
    edges_df = pd.read_csv(edges_path)


    # now we load the data but what about if the user upload edges.csv but this file have only to column and not having the from?
    # so we just need to make another check
    # cause the role is to not trust the user ever never
    
    if node_id_col not in nodes_df.columns:
        raise ValueError(
            f"Nodes file must contain '{node_id_col}' column. "
            f"Available columns: {list(nodes_df.columns)}"
        )

    if source_col not in edges_df.columns or target_col not in edges_df.columns:
        raise ValueError(
            f"Edges file must contain '{source_col}' and '{target_col}' columns. "
            f"Available columns: {list(edges_df.columns)}"
        )
    
    # now more checks about what if there is any missing values in the key columns
    if nodes_df[node_id_col].isnull().any():
        raise ValueError("Nodes file contains missing values in node ID column")

    if edges_df[source_col].isnull().any() or edges_df[target_col].isnull().any():
        raise ValueError("Edges file contains missing values in source/target columns")
    
    if nodes_df[node_id_col].duplicated().any():
        raise ValueError("Duplicate node IDs found in nodes file")
    


    # now we finish all validation things now lets start the next step which isssssss

    #starting create the graph
    # and we will use the networkx libraray to make that built in but creating it will deponds on if it is directed or not directed
    if directed:
        G=nx.DiGraph()
    else:
        G=nx.Graph()
    

    # now the next step is to add the nodes with its attributes in this empty graph
    # now each node will have its unique id and its dictinoary of its attributes
    for _, row in nodes_df.iterrows():
        node_id = row[node_id_col]
        attrs = row.drop(node_id_col).to_dict()
        G.add_node(node_id, **attrs)

    # now we fill the graph with the nodes now it is the turn of the edges
    valid_nodes = set(nodes_df[node_id_col])

    for _, row in edges_df.iterrows():
        source = row[source_col]
        target = row[target_col]
        if source not in valid_nodes or target not in valid_nodes:
            raise ValueError( f"Edge ({source}, {target}) this edge hasing not existed node")
        attrs = row.drop([source_col, target_col]).to_dict()
        G.add_edge(source, target, **attrs)

    return G
    




    


