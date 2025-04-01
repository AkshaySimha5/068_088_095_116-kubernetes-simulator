import threading
import time
from typing import Dict
from ..models.node import Node

class HealthMonitor:
    def __init__(self, node_manager):
        self.node_manager = node_manager
        self.monitoring = False
        self.monitor_thread = None
        
    def start_monitoring(self, interval=10):
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_nodes, args=(interval,))
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
            
    def _monitor_nodes(self, interval):
        while self.monitoring:
            self.node_manager.check_health()
            time.sleep(interval)
            
    def handle_node_failure(self, node_id: str):
        node = self.node_manager.get_node(node_id)
        if node and node.status == "unhealthy":
            # Reschedule pods from failed node
            self.node_manager.pod_scheduler.reschedule_pods_from_failed_node(node_id)