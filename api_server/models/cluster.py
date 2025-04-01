class Cluster:
    def __init__(self):
        self.nodes = []
        self.pods = []
        
    def add_node(self, node):
        self.nodes.append(node)
        
    def add_pod(self, pod):
        self.pods.append(pod)
        
    def to_dict(self):
        return {
            "node_count": len(self.nodes),
            "pod_count": len(self.pods)
        }