import time
from typing import Dict
from ..models.node import Node

class NodeManager:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.last_heartbeat: Dict[str, float] = {}

    def add_node(self, node_id: str, cpu_cores: int) -> Node:
        """Add node with either custom or generated ID"""
        if node_id in self.nodes:
            raise ValueError(f"Node ID {node_id} already exists")
        node = Node(node_id, cpu_cores)
        self.nodes[node_id] = node
        self.last_heartbeat[node_id] = time.time()
        return node

    def prune_inactive_nodes(self, timeout_sec=30):
        """Remove nodes that haven't sent heartbeats"""
        current_time = time.time()
        inactive_nodes = [
            node_id for node_id, last_time in self.last_heartbeat.items()
            if current_time - last_time > timeout_sec
        ]
        for node_id in inactive_nodes:
            del self.nodes[node_id]
            del self.last_heartbeat[node_id]