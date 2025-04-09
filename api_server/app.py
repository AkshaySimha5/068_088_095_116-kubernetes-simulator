from flask import Flask, render_template, request, jsonify
from flask_restful import Api
import time

# Import RESTful resources
from .routes.node_routes import NodeResource, NodesResource, NodeHeartbeatResource
from .routes.health_routes import HealthResource

app = Flask(__name__, template_folder='templates')
api = Api(app)

# -------------------------
# Node Manager (Week 2)
# -------------------------
class NodeManager:
    def __init__(self):
        self.nodes = {}
        self.heartbeat_timeout = 60

    def register_node(self, node_id, cpu_cores):
        self.nodes[node_id] = {
            'cpu_cores': cpu_cores,
            'available_cpu': cpu_cores,
            'pods': [],
            'status': 'healthy',
            'last_heartbeat': time.time()
        }

    def get_node(self, node_id):
        return self.nodes.get(node_id)

    def get_all_nodes(self):
        return self.nodes

    def prune_inactive_nodes(self):
        current_time = time.time()
        for node_id, node in list(self.nodes.items()):
            if current_time - node['last_heartbeat'] > self.heartbeat_timeout:
                node['status'] = 'unhealthy'

    def add_pod_to_node(self, node_id, pod):
        if node_id in self.nodes:
            self.nodes[node_id]['pods'].append(pod)

node_manager = NodeManager()

# -------------------------
# Pod Scheduler (Week 2)
# -------------------------
class PodScheduler:
    def __init__(self, node_manager):
        self.node_manager = node_manager

    def schedule_pod(self, cpu_required):
        """First-Fit scheduling algorithm"""
        nodes = self.node_manager.get_all_nodes()
        for node_id, node_data in nodes.items():
            if node_data["available_cpu"] >= cpu_required and node_data["status"] == "healthy":
                return node_id
        return None

# -------------------------
# Register API Resources
# -------------------------
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
    resource_class_kwargs={
        'node_manager': node_manager,
        'heartbeat_timeout': node_manager.heartbeat_timeout
    }
)
api.add_resource(
    HealthResource, '/health',
    resource_class_kwargs={'node_manager': node_manager}
)

# -------------------------
# Pod Scheduling Endpoint (Week 2)
# -------------------------
@app.route('/api/pods', methods=['POST'])
def launch_pod():
    data = request.get_json()
    if not data or 'cpu_required' not in data:
        return jsonify({"error": "Missing CPU requirement"}), 400

    try:
        cpu_required = float(data['cpu_required'])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid CPU value"}), 400

    scheduler = PodScheduler(node_manager)
    node_id = scheduler.schedule_pod(cpu_required)
    if not node_id:
        return jsonify({"error": "No healthy node with sufficient resources"}), 400

    pod_id = f"pod-{len(node_manager.nodes[node_id]['pods']) + 1}"
    pod = {'id': pod_id, 'cpu_required': cpu_required}

    node_manager.nodes[node_id]['available_cpu'] -= cpu_required
    node_manager.add_pod_to_node(node_id, pod)

    return jsonify({
        "message": "Pod scheduled successfully",
        "pod_id": pod_id,
        "node_id": node_id,
        "remaining_cpu": node_manager.nodes[node_id]['available_cpu']
    }), 201

# -------------------------
# HTML Dashboard
# -------------------------
@app.route('/')
def dashboard():
    node_manager.prune_inactive_nodes()
    return render_template(
        'index.html',
        nodes=node_manager.nodes,
        stats={
            'total_nodes': len(node_manager.nodes),
            'healthy_nodes': sum(1 for n in node_manager.nodes.values() if n['status'] == 'healthy'),
            'total_pods': sum(len(n['pods']) for n in node_manager.nodes.values())
        }
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
