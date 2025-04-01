import requests
import time
import threading
from typing import Dict, List

class NodeSimulator:
    def __init__(self, node_id: str, api_server_url: str, cpu_cores: int):
        self.node_id = node_id
        self.api_server_url = api_server_url
        self.cpu_cores = cpu_cores
        self.available_cpu = cpu_cores
        self.pods: List[str] = []
        self.running = False
        self.heartbeat_thread = None
        
    def start(self):
        self.running = True
        self._register_with_server()
        self.heartbeat_thread = threading.Thread(target=self._send_heartbeat)
        self.heartbeat_thread.daemon = True
        self.heartbeat_thread.start()
        
    def stop(self):
        self.running = False
        if self.heartbeat_thread:
            self.heartbeat_thread.join()
            
    def _register_with_server(self):
        url = f"{self.api_server_url}/nodes"
        data = {
            "node_id": self.node_id,
            "cpu_cores": self.cpu_cores
        }
        response = requests.post(url, json=data)
        if response.status_code != 201:
            raise Exception("Failed to register node with API server")
            
    def _send_heartbeat(self):
        while self.running:
            url = f"{self.api_server_url}/nodes/{self.node_id}/heartbeat"
            data = {
                "pods": self.pods,
                "available_cpu": self.available_cpu
            }
            try:
                requests.post(url, json=data)
            except requests.exceptions.RequestException as e:
                print(f"Heartbeat failed: {e}")
            time.sleep(5)
            
    def add_pod(self, pod_id: str, cpu_required: int):
        if cpu_required > self.available_cpu:
            raise ValueError("Not enough CPU available")
        self.pods.append(pod_id)
        self.available_cpu -= cpu_required
        
    def remove_pod(self, pod_id: str, cpu_allocated: int):
        if pod_id in self.pods:
            self.pods.remove(pod_id)
            self.available_cpu += cpu_allocated