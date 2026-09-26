# 🚀 Comprehensive Deployment & Setup Guide

This guide provides step-by-step instructions for setting up, building, and running **AeroCave-DRL-Pilot** across local development environments and multi-node production clusters.

---

## 📋 System Prerequisites

Ensure you have the following installed on your host system:
* **Operating System**: Linux (Ubuntu 22.04 LTS recommended) / Windows 11 with WSL2
* **Docker Engine**: v24.0 or higher
* **Docker Compose**: v2.20 or higher
* **Python**: v3.10
* **Node.js**: v18.x or higher
* **Expo CLI**: For mobile app preview (`npm install -g expo-cli`)

---

## 🛠️ Option 1: Local Development Setup (Docker Compose)

### 1. Environment Configuration
Create a `.env` file in the project root directory:

```env
POSTGRES_USER=aerocave_user
POSTGRES_PASSWORD=secure_password_123
POSTGRES_DB=aerocave_db
POSTGRES_PORT=5432

FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
WEBSOCKET_RATE_HZ=20

REACT_APP_WEBSOCKET_URL=ws://localhost:8000/ws/telemetry
2. Launch Stack Services
Run the following command to build and launch all containers in detached mode:

Bash
docker compose up -d --build
Figure 1: Successful initialization of all microservices via Docker Compose.

🌐 Option 2: Production Deployment (Docker Swarm)
For multi-node deployment with Traefik load balancing and automated health checks:

1. Initialize Swarm Cluster
Bash
docker swarm init
2. Deploy Stack
Bash
docker stack deploy -c docker-compose.yml aerocave_stack
Figure 2: Active Docker Swarm manager initializing service replicas.

📱 Mobile Client Setup (React Native / Expo)
To run the field technician mobile monitoring client:

Navigate to the mobile directory:

Bash
cd mobile_app
npm install
Start the Metro Bundler:

Bash
npx expo start
Figure 3: Metro Bundler output with Expo QR code for mobile device connection.

🧹 Maintenance & Cleanup
To stop and remove all running containers and networks:

Bash
# For Docker Compose
docker compose down -v

# For Docker Swarm
docker stack rm aerocave_stack