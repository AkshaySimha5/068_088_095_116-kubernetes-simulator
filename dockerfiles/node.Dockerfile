FROM python:3.9-slim
WORKDIR /app

# Install signal handling dependencies
RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

COPY node_simulator/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY node_simulator .

# Use shell form to allow signal propagation
CMD python node.py \
    --node-id ${NODE_ID:-docker-node-default} \
    --api-server http://host.docker.internal:5000 \
    --cpu-cores 2