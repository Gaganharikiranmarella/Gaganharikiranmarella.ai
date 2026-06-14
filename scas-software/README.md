# Swarm Control Artillery System (SCAS)

## AI-Driven Autonomous Counter-UAV Command and Control Platform

### Project Overview

The Swarm Control Artillery System (SCAS) is an AI-enabled battlefield intelligence and decision-support framework designed to detect, track, classify, and prioritize hostile Unmanned Aerial Vehicle (UAV) swarms operating within protected airspace. The platform integrates computer vision, swarm intelligence, machine learning, real-time telemetry analytics, and autonomous threat assessment to provide a software-defined counter-UAV solution.

Unlike conventional air-defense systems that focus on single-target engagement, SCAS is designed to handle coordinated multi-agent drone incursions through intelligent swarm analysis and predictive threat evaluation.

The platform functions as a real-time Command and Control (C2) environment capable of ingesting live video streams, detecting UAVs, assigning persistent identities, clustering cooperative swarm formations, forecasting movement trajectories, and generating threat intelligence for operators.

---

# Key Capabilities

* Real-Time UAV Detection
* Multi-Object Tracking
* Autonomous Swarm Identification
* Threat Prioritization Engine
* Tactical Airspace Visualization
* Trajectory Prediction
* Alert Generation
* Command Center Dashboard
* Historical Mission Replay
* Battlefield Analytics

---

# Operational Workflow

```text
Live Camera Feed
        │
        ▼
Video Acquisition Layer
        │
        ▼
Drone Detection Engine
(YOLO)
        │
        ▼
Multi-Object Tracking
(DeepSORT)
        │
        ▼
Swarm Clustering Engine
(Agglomerative Clustering)
        │
        ▼
Threat Assessment Engine
(Deep Neural Network)
        │
        ▼
Trajectory Prediction
(LSTM)
        │
        ▼
Command & Control Dashboard
        │
        ▼
Alert & Decision Support System
```

---

# System Architecture

```text
┌───────────────────────────────┐
│      Mobile Camera Feed       │
└───────────────┬───────────────┘
                │
                ▼

┌───────────────────────────────┐
│      FastAPI Backend          │
└───────────────┬───────────────┘

                │
      ┌─────────┼─────────┐

      ▼         ▼         ▼

Detection  Tracking   Database

 YOLO      DeepSORT    SQLite

      ▼         ▼

     Swarm Analytics

      ▼

Threat Intelligence

      ▼

Trajectory Forecasting

      ▼

WebSocket Gateway

      ▼

┌───────────────────────────────┐
│ React Tactical Dashboard      │
└───────────────────────────────┘
```

---

# Tactical Decision Pipeline

```text
Drone Detection

        ↓

Identity Assignment

        ↓

Swarm Formation Recognition

        ↓

Threat Evaluation

        ↓

Trajectory Forecast

        ↓

Risk Classification

        ↓

Alert Generation

        ↓

Operator Decision Support
```

---

# Artificial Intelligence Components

## Computer Vision Layer

Purpose:

Detection of aerial targets from live video streams.

Technology:

* YOLOv11
* OpenCV

Outputs:

* Bounding Box
* Confidence Score
* Object Class

---

## Tracking Layer

Purpose:

Persistent tracking of detected drones.

Technology:

* DeepSORT

Outputs:

* UAV Identifier
* Position History
* Velocity Vector

Example:

UAV-001
UAV-002
UAV-003

---

## Swarm Intelligence Layer

Purpose:

Identification of coordinated swarm formations.

Technology:

* Agglomerative Hierarchical Clustering

Inputs:

* Position
* Velocity
* Heading

Outputs:

Cluster Alpha
Cluster Bravo
Cluster Charlie

---

## Threat Assessment Layer

Purpose:

Threat prioritization and danger estimation.

Technology:

* Deep Neural Network
* ReLU Activation
* Softmax Classification

Threat Categories:

* Low
* Moderate
* High
* Critical

---

## Trajectory Prediction Layer

Purpose:

Future path forecasting.

Technology:

* LSTM Network

Outputs:

* Predicted Position
* ETA
* Impact Probability

---

# Mathematical Model

Distance between UAV and Protected Asset:

d = √[(x₂-x₁)² + (y₂-y₁)² + (z₂-z₁)²]

---

Threat Priority Index:

TPI = αP + βV + γD + δA

Where:

P = Proximity Score

V = Velocity Score

D = Density Score

A = Attack Alignment Score

α + β + γ + δ = 1

---

ReLU Activation:

f(x) = max(0,x)

---

Softmax Probability:

P(i) = exp(zᵢ) / Σ exp(zⱼ)

---

Sigmoid Threat Scaling:

T = 1 / (1 + e⁻ᵏ⁽ˣ⁻ᶜ⁾)

---

# Database Architecture

## drone_telemetry

Stores:

* Drone ID
* Coordinates
* Altitude
* Velocity
* Timestamp

---

## swarm_clusters

Stores:

* Cluster ID
* Swarm Size
* Average Velocity
* Threat Score

---

## threat_assessments

Stores:

* Threat Parameters
* Threat Classification
* Final Threat Score

---

## trajectory_predictions

Stores:

* Future Coordinates
* Confidence Score
* ETA

---

## alerts

Stores:

* Alert Severity
* Alert Type
* Generated Timestamp

---

# Frontend Features

## Tactical Dashboard

Displays:

* Active UAVs
* Active Swarms
* Threat Level
* Critical Alerts

---

## Tactical Airspace Map

Displays:

* Drone Positions
* Cluster Locations
* Protected Assets
* Predicted Trajectories

---

## Alert Center

Displays:

* Intrusion Alerts
* Swarm Alerts
* Critical Threat Notifications

---

## Mission Replay

Displays:

* Historical Drone Movements
* Swarm Evolution
* Threat Timeline

---

# Technology Stack

Frontend

* React
* TypeScript
* TailwindCSS
* Mapbox
* Recharts
* Socket.IO

Backend

* FastAPI
* Python
* OpenCV
* WebSockets

Artificial Intelligence

* YOLOv11
* DeepSORT
* TensorFlow
* Scikit-Learn
* LSTM

Database

* SQLite

Deployment

* Vercel
* Render
* Railway

---

# Future Enhancements

* Transformer-Based Threat Intelligence
* Reinforcement Learning Tactical Agent
* Multi-Camera Sensor Fusion
* Radar Integration
* Thermal Imaging Support
* Digital Twin Battlefield Environment
* Autonomous Countermeasure Recommendation Engine
* Multi-Node Command Center Architecture

---

# Authors

M. Gagan

Rema Varshini

K. Sreeja

Department of Artificial Intelligence and Machine Learning

Geethanjali College of Engineering and Technology

---

"AI-Driven Swarm Intelligence for Next-Generation Counter-UAV Defense Operations."
