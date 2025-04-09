# Kubernetes Cluster Simulator

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A lightweight simulation-based distributed system that mimics core Kubernetes cluster management functionalities, developed as part of UE22CS351B Cloud Computing course at PES University.

## Team Members
- PES1UG22CS068 - Akshay Simha L N
- PES1UG22CS088 - Anikait Nanjundappa .
- PES1UG22CS095 - Anish D B
- PES1UG22CS116 - Ashish Chandra K

## Features
- API Server with Node Management
- Pod Scheduling (First-Fit, Best-Fit, Worst-Fit algorithms)
- Health Monitoring with Heartbeat System
- Fault Tolerance and Pod Rescheduling
- CLI Interface for Cluster Management

## Commands

## Week 1
- python -m api_server.app
- python node_simulator/node.py --api-server http://localhost:5000 --cpu-cores 2
- docker build -f dockerfiles/node.Dockerfile -t node-sim .
- docker run --rm -e NODE_ID={ID} -e CPU_CORES={VAL} node-sim

## Week 2
- python -m api_server.app

# Build the Node Docker Image
- docker build -t node-sim ./node_simulator 

#  Start Simulated Nodes (Auto-register & send heartbeats)

   # Node 1 (2 CPU cores)
-  docker run -d --rm --name node-1 `
  -e NODE_ID=node-1 `
  -e CPU_CORES=2 `
  -e API_SERVER_URL=http://host.docker.internal:5000 `
   node-sim

   # Node 2 (4 CPU cores)
-  docker run -d --rm --name node-2 `
  -e NODE_ID=node-2 `
  -e CPU_CORES=4 `
  -e API_SERVER_URL=http://host.docker.internal:5000 `
  node-sim

   # Node 3 (1 CPU cores)
-  docker run -d --rm --name node-3 `
  -e NODE_ID=node-3 `
  -e CPU_CORES=1 `
  -e API_SERVER_URL=http://host.docker.internal:5000 `
  node-sim

# Schedule Pods to the Cluster
 
   # Schedule Pod (3 CPU cores):
   $body = @{ cpu_required = 3 } | ConvertTo-Json
   Invoke-RestMethod -Uri "http://localhost:5000/api/pods" `
  -Method Post -Body $body -ContentType "application/json"

   #  Schedule Pod (1 CPU core):
    $body = @{ cpu_required = 1 } | ConvertTo-Json
    Invoke-RestMethod -Uri "http://localhost:5000/api/pods" `
    -Method Post -Body $body -ContentType "application/json"

#  Monitor Cluster State
   
   #  Visit Real-Time Dashboard
   http://localhost:5000
   
# Stop Running Node Containers
  docker stop node-1 node-2 node-3







  
