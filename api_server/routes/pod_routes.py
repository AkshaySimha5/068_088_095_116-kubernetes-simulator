from flask_restful import Resource, reqparse
from ..managers.pod_scheduler import PodScheduler

parser = reqparse.RequestParser()
parser.add_argument('cpu_required', type=int, required=True)

class PodResource(Resource):
    def __init__(self, pod_scheduler: PodScheduler):
        self.pod_scheduler = pod_scheduler
        
    def get(self, pod_id):
        pod = self.pod_scheduler.get_pod(pod_id)
        if pod:
            return pod.to_dict(), 200
        return {"message": "Pod not found"}, 404

class PodsResource(Resource):
    def __init__(self, pod_scheduler: PodScheduler):
        self.pod_scheduler = pod_scheduler
        
    def get(self):
        return [pod.to_dict() for pod in self.pod_scheduler.get_all_pods()]
    
    def post(self):
        args = parser.parse_args()
        node = self.pod_scheduler.schedule_pod(args['cpu_required'])
        if node:
            return {"message": "Pod scheduled successfully", "node": node.node_id}, 201
        return {"message": "No available nodes with sufficient resources"}, 400