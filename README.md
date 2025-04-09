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
- python -m api_server.app
- python node_simulator/node.py --api-server http://localhost:5000 --cpu-cores 2
- docker build -f dockerfiles/node.Dockerfile -t node-sim .
- docker run --rm -e NODE_ID={ID} -e CPU_CORES={VAL} node-sim

  
