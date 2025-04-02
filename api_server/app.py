from flask import Flask
from flask_restful import Api
from .managers.node_manager import NodeManager
from .routes.node_routes import NodeResource, NodesResource

app = Flask(__name__)
api = Api(app)

# Initialize core components
node_manager = NodeManager()

# Register routes
api.add_resource(
    NodesResource, '/nodes',
    resource_class_kwargs={'node_manager': node_manager}
)
api.add_resource(
    NodeResource, '/nodes/<string:node_id>',
    resource_class_kwargs={'node_manager': node_manager}
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)