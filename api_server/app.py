from flask import Flask, render_template
from flask_restful import Api
from .managers.node_manager import NodeManager
from .routes.node_routes import NodeResource, NodesResource, NodeHeartbeatResource
from .routes.health_routes import HealthResource

app = Flask(__name__, template_folder='templates')
api = Api(app)

# Initialize core components
node_manager = NodeManager()

# RESTful API routes
api.add_resource(
    NodesResource, '/nodes',
    resource_class_kwargs={'node_manager': node_manager}
)
api.add_resource(
    NodeResource, '/nodes/<string:node_id>',
    resource_class_kwargs={'node_manager': node_manager}
)
api.add_resource(
    NodeHeartbeatResource, '/nodes/<string:node_id>/heartbeat',
    resource_class_kwargs={'node_manager': node_manager}
)
api.add_resource(
    HealthResource, '/health',
    resource_class_kwargs={'node_manager': node_manager}
)

# Web route for HTML dashboard
@app.route('/')
def dashboard():
    node_manager.prune_inactive_nodes()
    nodes = node_manager.get_all_nodes()
    return render_template('index.html', nodes=nodes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
