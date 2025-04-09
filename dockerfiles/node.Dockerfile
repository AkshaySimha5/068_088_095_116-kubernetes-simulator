FROM python:3.9-slim

WORKDIR /app

# Install required tools (procps for health checks, curl for debugging)
RUN apt-get update && \
    apt-get install -y procps curl && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY node_simulator/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy node simulator code
COPY node_simulator .

# Environment variables with defaults
ENV NODE_ID=default-node \
    API_SERVER_URL=http://api-server:5000 \
    CPU_CORES=2 \
    HEARTBEAT_INTERVAL=30

# Health check (verify heartbeat process is running)
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s \
    CMD ps aux | grep -q "[p]ython heartbeat_sender.py" || exit 1

# Run both node simulator and heartbeat sender in parallel
CMD bash -c "python node.py --node-id ${NODE_ID} --api-server ${API_SERVER_URL} --cpu-cores ${CPU_CORES} & \
    python heartbeat_sender.py --node-id ${NODE_ID} --api-server ${API_SERVER_URL} --interval ${HEARTBEAT_INTERVAL} && \
    fg %1"