from flask import Flask
from flask_restful import Api
from api_server.routes.node_routes import NodeResource, NodesResource
from api_server.routes.pod_routes import PodResource, PodsResource
from api_server.managers.node_manager import NodeManager
from api_server.managers.pod_scheduler import PodScheduler
from api_server.managers.health_monitor import HealthMonitor

app = Flask(__name__)
api = Api(app)

# Initialize managers
node_manager = NodeManager()
pod_scheduler = PodScheduler(node_manager)
health_monitor = HealthMonitor(node_manager)

# Add routes
api.add_resource(NodesResource, '/nodes', resource_class_kwargs={'node_manager': node_manager})
api.add_resource(NodeResource, '/nodes/<string:node_id>', resource_class_kwargs={'node_manager': node_manager})
api.add_resource(PodsResource, '/pods', resource_class_kwargs={'pod_scheduler': pod_scheduler})
api.add_resource(PodResource, '/pods/<string:pod_id>', resource_class_kwargs={'pod_scheduler': pod_scheduler})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)