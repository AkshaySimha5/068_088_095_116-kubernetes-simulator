class Node:
    def __init__(self, node_id: str, cpu_cores: int):
        self.node_id = node_id
        self.cpu_cores = cpu_cores
        self.available_cpu = cpu_cores  # Initially all cores available
        self.status = "healthy"  # or "unhealthy"

    def to_dict(self):
        return {
            "node_id": self.node_id,
            "cpu_cores": self.cpu_cores,
            "available_cpu": self.available_cpu,
            "status": self.status
        }