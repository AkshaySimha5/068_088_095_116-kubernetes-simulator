import threading
import time

class HealthMonitor:
    def __init__(self, node_manager):
        self.node_manager = node_manager
        self.monitoring = False
        self.monitor_thread = None
        
    def start_monitoring(self, interval=10):
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_nodes, 
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
        
    def _monitor_nodes(self, interval):
        while self.monitoring:
            self.node_manager.check_health()
            time.sleep(interval)