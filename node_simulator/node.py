import requests
import time
import threading
import argparse

class NodeSimulator:
    def __init__(self, node_id: str, api_server_url: str, cpu_cores: int):
        self.node_id = node_id
        self.api_server_url = api_server_url
        self.cpu_cores = cpu_cores
        self.running = False
        
    def start(self):
        self.running = True
        self._register_node()
        threading.Thread(target=self._send_heartbeat, daemon=True).start()
        
    def _register_node(self):
        response = requests.post(
            f"{self.api_server_url}/nodes",
            json={"cpu_cores": self.cpu_cores}
        )
        if response.status_code != 201:
            raise Exception("Failed to register node")
            
    def _send_heartbeat(self):
        while self.running:
            try:
                requests.post(
                    f"{self.api_server_url}/nodes/{self.node_id}/heartbeat",
                    json={"status": "healthy"}
                )
            except requests.exceptions.RequestException as e:
                print(f"Heartbeat failed: {e}")
            time.sleep(5)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--node-id', required=True)
    parser.add_argument('--api-server', required=True)
    parser.add_argument('--cpu-cores', type=int, required=True)
    args = parser.parse_args()
    
    node = NodeSimulator(args.node_id, args.api_server, args.cpu_cores)
    node.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        node.running = False