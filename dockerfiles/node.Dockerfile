FROM python:3.9-slim

WORKDIR /app

# Install required tools
RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY node_simulator/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy node simulator code
COPY node_simulator .

# Run node.py with environment-based args
CMD python node.py \
    --node-id ${NODE_ID:-docker-node-default} \
    --api-server http://host.docker.internal:5000 \
    --cpu-cores ${CPU_CORES:-2}
