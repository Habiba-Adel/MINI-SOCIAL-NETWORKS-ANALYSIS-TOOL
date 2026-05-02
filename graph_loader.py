import pandas as pd
import networkx as nx
import os


# we will define the function that will build the graph to make it reusable and can be used easily
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
    #optimization of our prev for loop
    G.add_nodes_from(nodes_df.set_index(node_id_col).to_dict('index').items())

    # now we fill the graph with the nodes now it is the turn of the edges
    valid_nodes = set(nodes_df[node_id_col])

   # Create True/False (to be faaasttttt) masks checking if sources/targets are NOT in valid_nodes
    invalid_sources = ~edges_df[source_col].isin(valid_nodes)
    invalid_targets = ~edges_df[target_col].isin(valid_nodes)
    
    # If any invalid edge exists, raise an error (check if true exists)
    if invalid_sources.any() or invalid_targets.any():
        # Grab the very first invalid row to show in the error message
        bad_row = edges_df[invalid_sources | invalid_targets].iloc[0]
        raise ValueError(f"Edge ({bad_row[source_col]}, {bad_row[target_col]}) contains a non-existent node.")

    # Add Edges
    # adds all edges and attributes using NetworkX's built-in Pandas reader
    extra_columns = [col for col in edges_df.columns if col not in [source_col, target_col]]
    
    # We load the edges into a TEMPORARY graph first
    temp_edge_graph = nx.from_pandas_edgelist(
        edges_df, 
        source=source_col, 
        target=target_col, 
        edge_attr=extra_columns if len(extra_columns) > 0 else None,
        create_using=nx.DiGraph() if directed else nx.Graph()
    )
    
    # Then we safely merge the edges into our main graph G (which keeps all node attributes safe!)
    G.add_edges_from(temp_edge_graph.edges(data=True))

    return G
    




    


