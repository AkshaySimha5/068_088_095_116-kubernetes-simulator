from typing import Optional
from ..models.node import Node
from ..models.pod import Pod
import uuid

class PodScheduler:
    def __init__(self, node_manager):
        self.node_manager = node_manager
        self.pods = {}
        
    def schedule_pod(self, cpu_required: int) -> Optional[Node]:
        pod_id = str(uuid.uuid4())
        # First-fit algorithm
        for node in self.node_manager.get_all_nodes():
            if node.status == "healthy" and node.available_cpu >= cpu_required:
                pod = Pod(pod_id, cpu_required, node.node_id)
                node.allocate_pod(pod)
                self.pods[pod_id] = pod
                return node
        return None
        
    def get_pod(self, pod_id: str) -> Optional[Pod]:
        return self.pods.get(pod_id)
        
    def get_all_pods(self) -> list:
        return list(self.pods.values())