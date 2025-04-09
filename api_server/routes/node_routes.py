from flask_restful import Resource, reqparse
from flask import request
from ..managers.node_manager import NodeManager
import time

parser = reqparse.RequestParser()
parser.add_argument('cpu_cores', type=int, required=True)
parser.add_argument('node_id', type=str, required=False)

class NodeResource(Resource):
    def __init__(self, node_manager: NodeManager):
        self.node_manager = node_manager

    def get(self, node_id):
        node = self.node_manager.get_node(node_id)
        if node:
            return node.to_dict(), 200
        return {"message": "Node not found"}, 404

class NodesResource(Resource):
    def __init__(self, node_manager: NodeManager):
        self.node_manager = node_manager

    def get(self):
        # Prune inactive nodes before returning the list
        self.node_manager.prune_inactive_nodes()
        return [
            {
                "node_id": node_id,
                **node_data
            } for node_id, node_data in self.node_manager.get_all_nodes().items()
        ], 200

    def post(self):
        args = parser.parse_args()
        node_id = args.get('node_id') or f"node-{len(self.node_manager.nodes) + 1}"
        self.node_manager.register_node(node_id, args['cpu_cores'])
        return {
            "node_id": node_id,
            **self.node_manager.nodes[node_id]
        }, 201

class NodeHeartbeatResource(Resource):
    def __init__(self, node_manager, heartbeat_timeout):
        self.node_manager = node_manager
        self.timeout = heartbeat_timeout

    def post(self, node_id):
        node = self.node_manager.nodes.get(node_id)
        if not node:
            return {"error": "Node not found"}, 404

        node['last_heartbeat'] = time.time()
        node['status'] = 'healthy'
        return {"status": "updated"}, 200
