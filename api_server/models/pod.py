class Pod:
    def __init__(self, pod_id, cpu_required, node_id=None):
        self.pod_id = pod_id
        self.cpu_required = cpu_required
        self.node_id = node_id
        
    def to_dict(self):
        return {
            "pod_id": self.pod_id,
            "cpu_required": self.cpu_required,
            "node_id": self.node_id
        }