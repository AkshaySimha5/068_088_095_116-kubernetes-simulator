class Node:
    def __init__(self, node_id, cpu_cores):
        self.node_id = node_id
        self.cpu_cores = cpu_cores
        self.available_cpu = cpu_cores
        self.pods = []
        self.status = "healthy"
        
    def allocate_pod(self, pod):
        if pod.cpu_required > self.available_cpu:
            raise ValueError("Not enough CPU available")
        self.pods.append(pod)
        self.available_cpu -= pod.cpu_required
        
    def to_dict(self):
        return {
            "node_id": self.node_id,
            "cpu_cores": self.cpu_cores,
            "available_cpu": self.available_cpu,
            "pod_count": len(self.pods),
            "status": self.status
        }