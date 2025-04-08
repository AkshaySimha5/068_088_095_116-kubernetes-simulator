from flask_restful import Resource, reqparse
from flask import request
from ..managers.node_manager import NodeManager

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
        self.node_manager.prune_inactive_nodes()
        return [n.to_dict() for n in self.node_manager.get_all_nodes()], 200

    def post(self):
        args = parser.parse_args()
        node_id = args.get('node_id') or f"node-{len(self.node_manager.nodes)+1}"
        node = self.node_manager.add_node(node_id, args['cpu_cores'])
        return node.to_dict(), 201

class NodeHeartbeatResource(Resource):
    def __init__(self, node_manager: NodeManager):
        self.node_manager = node_manager

    def post(self, node_id):
        data = request.get_json()
        available_cpu = data.get("available_cpu")
        if available_cpu is None:
            return {"message": "Missing available_cpu"}, 400

        success = self.node_manager.update_heartbeat(node_id, available_cpu)
        if success:
            return {"message": "Heartbeat received"}, 200
        return {"message": "Node not found"}, 404
