import customtkinter as ctk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import networkx as nx

from graph_loader import build_graph
from metrics import calculate_metrics
from community_detection import run_community_detection
from filtering import filter_by_centrality, filter_by_community
from evaluation import evaluation

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NetworkAnalystPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Graph Analyst Pro — Studio Edition")
        self.geometry("1300x850")

        self.G = None
        self.metrics = None
        self.community_results = None
        self.node_path = ""
        self.edge_path = ""

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkScrollableFrame(self, width=280, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(14, weight=1) 

        self.title_label = ctk.CTkLabel(self.sidebar, text="GRAPH ANALYST", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=30, pady=(40, 30))

        self.btn_nodes = ctk.CTkButton(self.sidebar, text="📁 Import Nodes CSV", fg_color="#6A5ACD", hover_color="#483D8B", height=40, font=ctk.CTkFont(size=13), command=self.browse_nodes)
        self.btn_nodes.grid(row=1, column=0, padx=30, pady=12, sticky="ew")

        self.btn_edges = ctk.CTkButton(self.sidebar, text="📁 Import Edges CSV", fg_color="#6A5ACD", hover_color="#483D8B", height=40, font=ctk.CTkFont(size=13), command=self.browse_edges)
        self.btn_edges.grid(row=2, column=0, padx=30, pady=12, sticky="ew")

        self.label_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Ground Truth Col (Optional)")
        self.label_entry.grid(row=3, column=0, padx=30, pady=5, sticky="ew")
 
        self.directed_var = ctk.BooleanVar(value=False)
        self.chk_directed = ctk.CTkCheckBox(self.sidebar, text="Directed Graph", variable=self.directed_var)
        self.chk_directed.grid(row=4, column=0, padx=30, pady=5, sticky="ew")

        self.btn_run = ctk.CTkButton(self.sidebar, text="🚀 RUN ANALYSIS", fg_color="#E91E63", hover_color="#C2185B", height=50, font=ctk.CTkFont(size=14, weight="bold"), command=self.process_data)
        self.btn_run.grid(row=5, column=0, padx=30, pady=20, sticky="ew")

        self.sep1 = ctk.CTkLabel(self.sidebar, text="—" * 20, text_color="gray")
        self.sep1.grid(row=6, column=0, pady=5)

        self.layout_label = ctk.CTkLabel(self.sidebar, text="Graph Layout", font=ctk.CTkFont(size=12))
        self.layout_label.grid(row=7, column=0, padx=30, pady=(5, 0), sticky="w")

        self.layout_menu = ctk.CTkOptionMenu(self.sidebar, values=["Spring", "Circular", "Shell", "Spectral"], fg_color="#333333", button_color="#444444", command=lambda _: self.draw_network(self.G))
        self.layout_menu.grid(row=8, column=0, padx=30, pady=10, sticky="ew")

        self.sep2 = ctk.CTkLabel(self.sidebar, text="—" * 20, text_color="gray")
        self.sep2.grid(row=9, column=0, pady=5)

        self.filter_label = ctk.CTkLabel(self.sidebar, text="Filtering Options", font=ctk.CTkFont(size=12, weight="bold"))
        self.filter_label.grid(row=10, column=0, padx=30, pady=(5, 0), sticky="w")

        self.filter_menu = ctk.CTkOptionMenu(self.sidebar, values=["None", "Degree", "Betweenness", "Closeness", "Pagerank", "Community"], fg_color="#333333", button_color="#444444")
        self.filter_menu.grid(row=11, column=0, padx=30, pady=10, sticky="ew")

        self.filter_min = ctk.CTkEntry(self.sidebar, placeholder_text="Min Val / Comm ID")
        self.filter_min.grid(row=12, column=0, padx=30, pady=5, sticky="ew")

        self.filter_max = ctk.CTkEntry(self.sidebar, placeholder_text="Max Val")
        self.filter_max.grid(row=13, column=0, padx=30, pady=5, sticky="ew")

        self.btn_filter = ctk.CTkButton(self.sidebar, text="🔍 Apply Filter", fg_color="#008CBA", hover_color="#005f7a", height=35, font=ctk.CTkFont(size=13, weight="bold"), command=self.apply_filter)
        self.btn_filter.grid(row=14, column=0, padx=30, pady=15, sticky="ew")

        self.main_container = ctk.CTkTabview(self, segmented_button_selected_color="#E91E63", segmented_button_unselected_hover_color="#6A5ACD")
        self.main_container.grid(row=0, column=1, padx=25, pady=25, sticky="nsew")
        
        self.tab_viz = self.main_container.add("Visualization")
        self.tab_eval = self.main_container.add("Community Evaluation")
        self.tab_stats = self.main_container.add("Network Statistics")
        self.stats_textbox = ctk.CTkTextbox(self.tab_stats, font=ctk.CTkFont(family="Consolas", size=15))
        self.stats_textbox.pack(fill="both", expand=True, padx=10, pady=10)

        self.fig, self.ax = plt.subplots(figsize=(8, 6), facecolor='#1A1A1A')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab_viz)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        self.toolbar_frame = ctk.CTkFrame(self.tab_viz, height=40, fg_color="transparent")
        self.toolbar_frame.pack(side="bottom", fill="x")
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.pack(pady=5)

        self.eval_textbox = ctk.CTkTextbox(self.tab_eval, font=ctk.CTkFont(family="Consolas", size=15))
        self.eval_textbox.pack(fill="both", expand=True, padx=10, pady=10)

    def browse_nodes(self):
        self.node_path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if self.node_path:
            self.btn_nodes.configure(text="✅ Nodes Loaded", fg_color="#2E7D32")

    def browse_edges(self):
        self.edge_path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if self.edge_path:
            self.btn_edges.configure(text="✅ Edges Loaded", fg_color="#2E7D32")

    def process_data(self):
        if not self.node_path or not self.edge_path:
            messagebox.showerror("Missing Data", "Please select both Nodes and Edges CSV files!")
            return
        try:
            is_directed = self.directed_var.get()
            self.G = build_graph(self.node_path, self.edge_path, directed=is_directed)
            self.G = build_graph(self.node_path, self.edge_path)
            self.metrics, _ = calculate_metrics(self.G)
            stats_text = "=== NETWORK METRICS ===\n\n"
            stats_text += f"Total Nodes: {self.G.number_of_nodes()}\n"
            stats_text += f"Total Edges: {self.G.number_of_edges()}\n\n"

            # Sort nodes to find the top influencer by PageRank (Link Analysis)
            sorted_pagerank = sorted(self.metrics.items(), key=lambda x: x[1]['Pagerank'], reverse=True)

            stats_text += "--- TOP 5 INFLUENCERS (PageRank) ---\n"
            for node, data in sorted_pagerank[:5]:
               stats_text += f"Node {node}: {data['Pagerank']:.4f}\n"

            self.stats_textbox.delete("1.0", "end")
            self.stats_textbox.insert("1.0", stats_text)
            self.community_results = run_community_detection(self.G)
            
            self.draw_network(self.G)
            self.run_evaluation_comparison()
            
            self.main_container.set("Visualization")
        except Exception as e:
            messagebox.showerror("Graph Error", f"Something went wrong: {e}")

    def run_evaluation_comparison(self):
        gn_comms = self.community_results["girvan_newman"]["communities"]
        louvain_comms = self.community_results["louvain"]["communities"]

        truth_col = self.label_entry.get().strip()
        label_to_pass = truth_col if truth_col != "" else None

        gn_eval = evaluation(self.G, gn_comms, label_name=label_to_pass)
        louvain_eval = evaluation(self.G, louvain_comms, label_name=label_to_pass)

        # تصميم الجدول
        text = "=======================================================================\n"
        text += "             COMMUNITY DETECTION ALGORITHMS COMPARISON\n"
        text += "=======================================================================\n\n"
        text += f"{'Metric':<25} | {'Girvan-Newman':<20} | {'Louvain':<20}\n"
        text += "-" * 70 + "\n"
        
        text += f"{'No. of Communities':<25} | {gn_eval['Number of Communities']:<20} | {louvain_eval['Number of Communities']:<20}\n"
        text += f"{'Modularity (0 to 1)':<25} | {gn_eval['Modularity']:<20.4f} | {louvain_eval['Modularity']:<20.4f}\n"
        text += f"{'Avg Conductance':<25} | {gn_eval['Average Conductance']:<20.4f} | {louvain_eval['Average Conductance']:<20.4f}\n"
        
        nmi_gn = gn_eval.get('NMI', 0)
        nmi_lv = louvain_eval.get('NMI', 0)
        if isinstance(nmi_gn, float):
            text += f"{'NMI Score (0 to 1)':<25} | {nmi_gn:<20.4f} | {nmi_lv:<20.4f}\n\n"
        else:
            text += f"{'NMI Score':<25} | {str(nmi_gn):<20} | {str(nmi_lv):<20}\n\n"
            
        text += "-" * 70 + "\n\n"

        best_alg = "Louvain" if louvain_eval['Modularity'] > gn_eval['Modularity'] else "Girvan-Newman"
        text += f"🏆 Recommendation:\nBased on Modularity, '{best_alg}' algorithm performs better on this network.\n(Higher Modularity indicates stronger and more distinct community structure)."

        self.eval_textbox.delete("1.0", "end")
        self.eval_textbox.insert("1.0", text)

    def apply_filter(self):
        if not self.G:
            messagebox.showerror("Error", "Please RUN ANALYSIS first!")
            return
        
        filter_type = self.filter_menu.get()
        if filter_type == "None":
            self.draw_network(self.G)
            return
        
        try:
            val1 = float(self.filter_min.get())
            
            if filter_type == "Community":
                filtered_G = filter_by_community(self.G, "louvain_community", int(val1))
            else:
                val2 = float(self.filter_max.get())
                filtered_G = filter_by_centrality(self.G, self.metrics, filter_type, val1, val2)
            
            if filtered_G.number_of_nodes() == 0:
                messagebox.showwarning("Empty Graph", "No nodes match these filter criteria!")
            else:
                self.draw_network(filtered_G)
                self.main_container.set("Visualization")
                
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers in the filter boxes!")

    def draw_network(self, graph_to_draw):
     if not graph_to_draw:
        return
        
     self.ax.clear()
     self.ax.set_axis_off()

      # Get positions
     pos = nx.spring_layout(graph_to_draw) # Add your layout logic here
    
    # Dynamically scale sizes based on Degree Centrality!
    # Multiply degree by a factor to make differences visually obvious
     node_sizes = []
     for node in graph_to_draw.nodes():
        # Fallback to 1 if node isn't in metrics (e.g., after filtering)
        degree = self.metrics.get(node, {}).get("Degree", 0.1) 
        node_sizes.append(300 + (degree * 2000))

    # Color by Louvain Community
     color_map = [graph_to_draw.nodes[node].get('louvain_community', 0) for node in graph_to_draw.nodes()]

     nx.draw(graph_to_draw, pos, ax=self.ax, with_labels=True,
            node_color=color_map, cmap=plt.cm.tab10, 
            node_size=node_sizes, edge_color="#888888", width=1.0,
            alpha=0.9, font_color="white", font_size=9, font_weight="bold")

     self.canvas.draw()

if __name__ == "__main__":
    app = NetworkAnalystPro()
    app.mainloop()