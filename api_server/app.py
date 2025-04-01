from flask import Flask
from flask_restful import Api
from .managers.node_manager import NodeManager
from .managers.pod_scheduler import PodScheduler
from .managers.health_monitor import HealthMonitor
from .routes.node_routes import NodeResource, NodesResource
from .routes.pod_routes import PodResource, PodsResource
from .routes.health_routes import HealthResource

app = Flask(__name__)
api = Api(app)

# Initialize managers
node_manager = NodeManager()
pod_scheduler = PodScheduler(node_manager)
health_monitor = HealthMonitor(node_manager)

# Start health monitoring
health_monitor.start_monitoring()

# Add routes
api.add_resource(
    NodesResource, '/nodes',
    resource_class_kwargs={'node_manager': node_manager}
)
api.add_resource(
    NodeResource, '/nodes/<string:node_id>',
    resource_class_kwargs={'node_manager': node_manager}
)
api.add_resource(
    PodsResource, '/pods',
    resource_class_kwargs={'pod_scheduler': pod_scheduler}
)
api.add_resource(
    PodResource, '/pods/<string:pod_id>',
    resource_class_kwargs={'pod_scheduler': pod_scheduler}
)
api.add_resource(
    HealthResource, '/health',
    resource_class_kwargs={'node_manager': node_manager}
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)