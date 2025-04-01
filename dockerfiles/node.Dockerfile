FROM python:3.9-slim
WORKDIR /app
COPY node_simulator/requirements.txt .
RUN pip install -r requirements.txt
COPY node_simulator .
CMD ["python", "node.py", "--node-id", "node1", "--api-server", "http://api-server:5000", "--cpu-cores", "4"]