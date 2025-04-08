import time
from typing import Dict
from ..models.node import Node

class NodeManager:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.last_heartbeat: Dict[str, float] = {}

    def add_node(self, node_id: str, cpu_cores: int) -> Node:
        """
        Add a new node to the cluster.
        Raises ValueError if node_id already exists.
        """
        if node_id in self.nodes:
            raise ValueError(f"Node ID {node_id} already exists")
        node = Node(node_id, cpu_cores)
        self.nodes[node_id] = node
        self.last_heartbeat[node_id] = time.time()
        return node

    def get_node(self, node_id: str) -> Node:
        """
        Retrieve a single node by its ID.
        Returns None if not found.
        """
        return self.nodes.get(node_id)

    def get_all_nodes(self):
        """
        Return a list of all node objects.
        """
        return list(self.nodes.values())

    def prune_inactive_nodes(self, timeout_sec=30):
        """
        Mark nodes as unhealthy if they haven't sent a heartbeat within the timeout.
        """
        current_time = time.time()
        for node_id, last_time in self.last_heartbeat.items():
            node = self.nodes[node_id]
            if current_time - last_time > timeout_sec:
                node.status = "unhealthy"
            else:
                node.status = "healthy"

    def update_heartbeat(self, node_id: str, available_cpu: int) -> bool:
        """
        Update the heartbeat and available CPU for the given node.
        Returns False if node is not found.
        """
        if node_id not in self.nodes:
            return False
        self.last_heartbeat[node_id] = time.time()
        self.nodes[node_id].available_cpu = available_cpu
        self.nodes[node_id].status = "healthy"
        return True
