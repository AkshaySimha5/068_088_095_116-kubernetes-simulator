import requests
import time
import os
import signal
import sys
import argparse

class NodeSimulator:
    def __init__(self, node_id, api_url, cpu_cores):
        self.node_id = node_id or os.getenv('NODE_ID', f"node-{os.urandom(4).hex()}")
        self.api_url = api_url
        self.cpu_cores = cpu_cores
        self.running = True

        # Handle graceful shutdown
        signal.signal(signal.SIGTERM, self.graceful_shutdown)
        signal.signal(signal.SIGINT, self.graceful_shutdown)

    def graceful_shutdown(self, signum, frame):
        print(f"Shutting down node {self.node_id}")
        self.running = False

    def _register(self):
        """Register node with the API server"""
        response = requests.post(
            f"{self.api_url}/nodes",
            json={
                "node_id": self.node_id,
                "cpu_cores": self.cpu_cores
            }
        )
        if not response.ok:
            raise Exception(f"Registration failed: {response.text}")
        print(f"Registered node {self.node_id}")

    def _send_heartbeat(self):
        """Send heartbeat to API server"""
        try:
            requests.post(
                f"{self.api_url}/nodes/{self.node_id}/heartbeat",
                json={"available_cpu": self.cpu_cores}
            )
        except Exception as e:
            print(f"Heartbeat failed: {e}")

    def start(self):
        """Main execution loop"""
        self._register()
        while self.running:
            self._send_heartbeat()
            time.sleep(5)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--node-id', required=False)
    parser.add_argument('--api-server', required=True)
    parser.add_argument('--cpu-cores', type=int, required=True)
    args = parser.parse_args()

    node = NodeSimulator(args.node_id, args.api_server, args.cpu_cores)
    node.start()