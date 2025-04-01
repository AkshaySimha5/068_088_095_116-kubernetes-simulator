FROM python:3.9-slim

WORKDIR /app

COPY node_simulator/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY node_simulator .

CMD ["python", "node.py"]