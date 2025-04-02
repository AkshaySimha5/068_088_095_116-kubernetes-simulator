from flask_restful import Resource, reqparse
from ..managers.node_manager import NodeManager

parser = reqparse.RequestParser()
parser.add_argument('cpu_cores', type=int, required=True)
parser.add_argument('node_id', type=str, required=False)  # Optional custom ID

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
        return [n.to_dict() for n in self.node_manager.nodes.values()]

    def post(self):
        args = parser.parse_args()
        node_id = args.get('node_id') or f"node-{len(self.node_manager.nodes)+1}"
        node = self.node_manager.add_node(node_id, args['cpu_cores'])
        return node.to_dict(), 201