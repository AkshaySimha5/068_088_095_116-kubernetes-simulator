import time
from typing import Dict, List
from ..models.node import Node

class NodeManager:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.last_heartbeat: Dict[str, float] = {}
        
    def add_node(self, node_id: str, cpu_cores: int) -> Node:
        node = Node(node_id, cpu_cores)
        self.nodes[node_id] = node
        self.last_heartbeat[node_id] = time.time()
        return node
        
    def get_node(self, node_id: str) -> Node:
        return self.nodes.get(node_id)
        
    def get_all_nodes(self) -> List[Node]:
        return list(self.nodes.values())
        
    def update_node_status(self, node_id: str, status: str):
        if node_id in self.nodes:
            self.nodes[node_id].status = status
            
    def record_heartbeat(self, node_id: str):
        self.last_heartbeat[node_id] = time.time()
        self.update_node_status(node_id, "healthy")
        
    def check_health(self, timeout_seconds=30):
        current_time = time.time()
        for node_id, last_time in self.last_heartbeat.items():
            if current_time - last_time > timeout_seconds:
                self.update_node_status(node_id, "unhealthy")