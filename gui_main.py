import customtkinter as ctk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import networkx as nx

# Import our modules
from graph_loader import build_graph
from metrics import calculate_metrics
from community_detection import run_community_detection
from filtering import filter_by_centrality

# Set the appearance mode and color theme for a modern look
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class NetworkAnalystPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Graph Analyst Pro — Studio Edition")
        self.geometry("1300x850")

        # State
        self.G = None
        self.metrics = None
        # Store file paths for later use once we select them
        self.node_path = ""
        self.edge_path = ""

        # UI Grid Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(
            7, weight=1)  # Push bottom elements down

        self.title_label = ctk.CTkLabel(
            self.sidebar, text="GRAPH ANALYST", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=30, pady=(40, 30))

        # Import Buttons
        # When this button clicked handle browse_nodes function
        self.btn_nodes = ctk.CTkButton(
            self.sidebar, text="📁 Import Nodes CSV",
            fg_color="#6A5ACD", hover_color="#483D8B",  # Lavender theme
            height=40, font=ctk.CTkFont(size=13),
            command=self.browse_nodes)
        self.btn_nodes.grid(row=1, column=0, padx=30, pady=12, sticky="ew")

        self.btn_edges = ctk.CTkButton(
            self.sidebar, text="📁 Import Edges CSV",
            fg_color="#6A5ACD", hover_color="#483D8B",
            height=40, font=ctk.CTkFont(size=13),
            command=self.browse_edges)
        self.btn_edges.grid(row=2, column=0, padx=30, pady=12, sticky="ew")

        self.btn_run = ctk.CTkButton(
            self.sidebar, text="🚀 RUN ANALYSIS",
            fg_color="#E91E63", hover_color="#C2185B",  # Bold Pink
            height=50, font=ctk.CTkFont(size=14, weight="bold"),
            command=self.process_data)
        self.btn_run.grid(row=3, column=0, padx=30, pady=40, sticky="ew")

        # Visual Controls Section
        self.sep = ctk.CTkLabel(self.sidebar, text="—" * 20, text_color="gray")
        self.sep.grid(row=4, column=0, pady=5)

        self.layout_label = ctk.CTkLabel(
            self.sidebar, text="Graph Layout Algorithm", font=ctk.CTkFont(size=12))
        self.layout_label.grid(row=5, column=0, padx=30,
                               pady=(15, 0), sticky="w")

        self.layout_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Spring", "Circular", "Shell", "Spectral"],
            fg_color="#333333", button_color="#444444",
            command=lambda _: self.draw_network())
        self.layout_menu.grid(row=6, column=0, padx=30, pady=15, sticky="ew")

        # --- MAIN VIEW ---
        self.main_container = ctk.CTkTabview(
            self, segmented_button_selected_color="#E91E63", segmented_button_unselected_hover_color="#6A5ACD")
        self.main_container.grid(
            row=0, column=1, padx=25, pady=25, sticky="nsew")
        self.tab_viz = self.main_container.add("Visualization")

        # Matplotlib Area
        # Using a slightly darker charcoal for the background to make the pink nodes "pop"
        self.fig, self.ax = plt.subplots(figsize=(8, 6), facecolor='#1A1A1A')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab_viz)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

        # Style the toolbar to be less intrusive
        self.toolbar_frame = ctk.CTkFrame(
            self.tab_viz, height=40, fg_color="transparent")
        self.toolbar_frame.pack(side="bottom", fill="x")
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.pack(pady=5)

    # Hanlde browse nodes and edges to select files and update button states accordingly
    def browse_nodes(self):
        self.node_path = filedialog.askopenfilename(
            filetypes=[("CSV", "*.csv")])
        if self.node_path:
            self.btn_nodes.configure(text="✅ Nodes Loaded", fg_color="#2E7D32")

    def browse_edges(self):
        self.edge_path = filedialog.askopenfilename(
            filetypes=[("CSV", "*.csv")])
        if self.edge_path:
            self.btn_edges.configure(text="✅ Edges Loaded", fg_color="#2E7D32")

    # This will called when we click run analysis, it will build the graph, calculate metrics, run community detection and then draw the network
    def process_data(self):
        if not self.node_path or not self.edge_path:
            messagebox.showerror(
                "Missing Data", "Please select both Nodes and Edges CSV files before running analysis!")
            return
        try:
            self.G = build_graph(self.node_path, self.edge_path)
            self.metrics, _ = calculate_metrics(self.G)
            # Run community detection and store in G attributes
            run_community_detection(self.G)
            self.draw_network()
        except Exception as e:
            messagebox.showerror(
                "Graph Error", f"Something went wrong while processing: {e}")

    # This will draw the graph with our results
    def draw_network(self):
        if not self.G:
            return
        self.ax.clear()
        self.ax.set_axis_off()

        choice = self.layout_menu.get().lower()
        try:
            if choice == "circular":
                pos = nx.circular_layout(self.G)
            elif choice == "shell":
                pos = nx.shell_layout(self.G)
            elif choice == "spectral":
                pos = nx.spectral_layout(self.G)
            else:
                pos = nx.spring_layout(self.G, k=0.15, iterations=50)
        except:
            pos = nx.spring_layout(self.G)  # Fallback

        # Use the Louvain community for coloring (your task!)
        color_map = []
        for node in self.G.nodes():
            # Providing a default color if community isn't found
            color_map.append(self.G.nodes[node].get('louvain_community', 0))

        # Refined drawing parameters
        nx.draw(self.G, pos, ax=self.ax, with_labels=True,
                node_color=color_map,
                cmap=plt.cm.spring,  # Bright pink/yellow colormap
                node_size=1000,
                edge_color="#444444",
                width=1.5,
                alpha=0.9,
                font_color="white",
                font_size=10,
                font_weight="bold")

        self.canvas.draw()


if __name__ == "__main__":
    app = NetworkAnalystPro()
    app.mainloop()
