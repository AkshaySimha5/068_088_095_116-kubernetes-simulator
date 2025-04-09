from flask import Flask, render_template, request, jsonify
from flask_restful import Api
import time

# Import RESTful resources
from .routes.node_routes import NodeResource, NodesResource, NodeHeartbeatResource
from .routes.health_routes import HealthResource

app = Flask(__name__, template_folder='templates')
api = Api(app)

# -------------------------
# Node Manager
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

    def delete_node(self, node_id):
        if node_id in self.nodes:
            del self.nodes[node_id]
            return True
        return False

    def prune_inactive_nodes(self):
        current_time = time.time()
        for node_id, node in list(self.nodes.items()):
            if current_time - node['last_heartbeat'] > self.heartbeat_timeout:
                if node['status'] == 'healthy':
                    node['status'] = 'unhealthy'
                    self._reschedule_pods(node_id)

    def _reschedule_pods(self, failed_node_id):
        failed_node = self.nodes.get(failed_node_id)
        if not failed_node:
            return

        pods_to_reschedule = failed_node['pods']
        failed_node['pods'] = []

        scheduler = PodScheduler(self)
        for pod in pods_to_reschedule:
            new_node_id = scheduler.schedule_pod(pod['cpu_required'])
            if new_node_id:
                self.nodes[new_node_id]['available_cpu'] -= pod['cpu_required']
                self.add_pod_to_node(new_node_id, pod)
                print(f"Rescheduled {pod['id']} from {failed_node_id} to {new_node_id}")
            else:
                print(f"Failed to reschedule pod {pod['id']} from {failed_node_id}")

    def add_pod_to_node(self, node_id, pod):
        if node_id in self.nodes:
            self.nodes[node_id]['pods'].append(pod)

    def remove_pod(self, pod_id):
        for node_id, node in self.nodes.items():
            for pod in node['pods']:
                if pod['id'] == pod_id:
                    node['pods'].remove(pod)
                    node['available_cpu'] += pod['cpu_required']
                    return True
        return False

node_manager = NodeManager()

# -------------------------
# Pod Scheduler
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
# Pod Scheduling Endpoint
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
# Pod Removal Endpoint (New)
# -------------------------
@app.route('/api/pods/remove', methods=['POST'])
def remove_pod():
    data = request.get_json()
    if not data or 'pod_id' not in data:
        return jsonify({"error": "Missing pod ID"}), 400

    pod_id = data['pod_id']
    success = node_manager.remove_pod(pod_id)
    if success:
        return jsonify({"message": f"Pod {pod_id} unscheduled successfully"}), 200
    else:
        return jsonify({"error": "Pod not found"}), 404

# -------------------------
# Delete Node Endpoint (New)
# -------------------------
@app.route('/api/nodes/<node_id>', methods=['DELETE'])
def delete_node(node_id):
    success = node_manager.delete_node(node_id)
    if success:
        return jsonify({"message": f"Node {node_id} deleted successfully"}), 200
    else:
        return jsonify({"error": "Node not found"}), 404

# -------------------------
# HTML Dashboard
# -------------------------
@app.route('/')
def dashboard():
    node_manager.prune_inactive_nodes()
    nodes = node_manager.get_all_nodes()
    return render_template(
        'index.html',
        nodes=nodes,
        stats={
            'total_nodes': len(nodes),
            'healthy_nodes': sum(1 for n in nodes.values() if n['status'] == 'healthy'),
            'unhealthy_nodes': sum(1 for n in nodes.values() if n['status'] == 'unhealthy'),
            'idle_nodes': sum(1 for n in nodes.values() if n['available_cpu'] == n['cpu_cores']),
            'total_pods': sum(len(n['pods']) for n in nodes.values())
        }
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
