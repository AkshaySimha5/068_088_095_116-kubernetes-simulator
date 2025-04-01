from flask_restful import Resource
from ..managers.node_manager import NodeManager

class HealthResource(Resource):
    def __init__(self, node_manager: NodeManager):
        self.node_manager = node_manager
        
    def get(self):
        healthy_nodes = [
            node for node in self.node_manager.get_all_nodes() 
            if node.status == "healthy"
        ]
        return {
            "total_nodes": len(self.node_manager.nodes),
            "healthy_nodes": len(healthy_nodes),
            "unhealthy_nodes": len(self.node_manager.nodes) - len(healthy_nodes)
        }, 200