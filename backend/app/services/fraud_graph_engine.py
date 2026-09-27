import networkx as nx

class FraudGraphEngine:
    def __init__(self):
        self.graph = nx.Graph()

    def add_node(self, case_id: str, id_number: str):
        self.graph.add_node(case_id, type="CASE")
        if id_number:
            self.graph.add_node(id_number, type="ID_NUMBER")
            self.graph.add_edge(case_id, id_number)

    def get_cluster(self, case_id: str) -> dict:
        if case_id not in self.graph:
            return {"nodes": [], "edges": [], "cluster_risk": 0, "connected_cases": 0}
        cluster_nodes = nx.node_connected_component(self.graph, case_id)
        subgraph = self.graph.subgraph(cluster_nodes)
        return {
            "case_id": case_id,
            "connected_cases": len(subgraph),
            "nodes": list(subgraph.nodes(data=True)),
            "edges": list(subgraph.edges(data=True))
        }
