# 🔗 Mini Social Networks Analysis Tool

A desktop-based network analysis and visualization platform that allows data analysts and researchers to explore, interact with, and analyze graph networks. Users can visualize network structures, detect communities, identify influential nodes, apply filtering, and compare link analysis techniques and all through an interactive interface.

---

## 📋 Project Requirements

- **Node & Edge Attributes** — Define and visualize custom attributes such as size, color, label, and shape
- **Layout Algorithms** — Force-directed (Fruchterman-Reingold), hierarchical, tree, and radial layouts
- **Graph Metrics & Statistics** — Degree distribution, clustering coefficient, average path length
- **Filtering Options** — Filter nodes by centrality measures (at least 3), community membership, or centrality score ranges
- **Community Detection** — Compare Girvan-Newman and Louvain algorithms side by side with modularity scores and evaluation metrics
- **Clustering Evaluation** — At least 3 internal and external community detection evaluations
- **Link Analysis** — PageRank, Betweenness Centrality, and other techniques to identify important nodes
- **Graph Loading** — Load networks via two CSV files (nodes + edges), supports both directed and undirected graphs

---

## 🚀 Get Started

### 1. Clone the Repository

```bash
git clone https://github.com/Habiba-Adel/MINI-SOCIAL-NETWORKS-ANALYSIS-TOOL.git
cd MINI-SOCIAL-NETWORKS-ANALYSIS-TOOL
```

---

### 2. Create a Virtual Environment

**Windows**
```bash
python -m venv venv
```

**macOS / Linux**
```bash
python3 -m venv venv
```

---

### 3. Activate the Virtual Environment

**Windows**
```bash
venv\Scripts\activate
```

**macOS / Linux**
```bash
source venv/bin/activate
```

> You should see `(venv)` appear at the start of your terminal line — that means it's active.

---

### 4. Install Dependencies

**Windows**
```bash
pip install pandas networkx
```

**macOS / Linux**
```bash
pip3 install pandas networkx
```

---

### 5. Run the Project

**Windows**
```bash
python main.py
```

**macOS / Linux**
```bash
python3 main.py
```

---

### 6. Deactivate the Virtual Environment (when done)

```bash
deactivate
```
