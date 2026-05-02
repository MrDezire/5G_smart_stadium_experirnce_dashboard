# Smart Stadium 5G Experience Dashboard 🏟️⚡

A high-performance, cinematic, and real-time operations dashboard for 5G stadium management. This project visualizes live network health, crowd analytics, fan engagement, and security signals in a single, immersive command-and-control surface.

![Dashboard Preview](https://github.com/MrDezire/5G_smart_stadium_experirnce_dashboard/raw/main/preview.png) *(Note: Add your own screenshot to the repo and update this link)*

## 🚀 Overview

This is a full-stack application designed to feel like a modern 5G operations room. It features a rich, dark-themed UI with glassmorphism and pulsing gold/crimson accents, powered by a real-time WebSocket backend.

### Key Features
- **Real-time 5G Metrics**: Live tracking of Latency (ms), Bandwidth (Gbps), and Connected Devices.
- **Network Slicing Monitoring**: Visualization of eMBB, URLLC, and mMTC slice health and load.
- **Crowd Density Mapping**: Live occupancy monitoring for stadium sections, gates, and concourses.
- **Fan Experience Analytics**: Real-time stats for AR/VR stream quality, app engagement, and merchandise sales.
- **Security Control Panel**: Monitoring of camera mesh status, access control variance, and incident routing.
- **Cinematic UI**: Fully responsive design (Mobile, Tablet, Desktop) with smooth scroll animations, depth effects, and glassmorphic panels.

---

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework for API and WebSocket handling.
- **WebSockets**: Bi-directional real-time data streaming.
- **Uvicorn**: ASGI server for running the application.

### Frontend
- **HTML5 & Vanilla CSS**: Modern CSS Grid/Flexbox layout with custom animations.
- **Vanilla JavaScript**: Lightweight WebSocket client logic with exponential backoff reconnect.
- **Google Fonts**: Orbitron (Numbers), Bebas Neue (Headers), and Rajdhani (Data).

---

## ⚙️ How It Works

1.  **Backend Simulation**: The `main.py` server runs a background loop that evolves a simulated stadium state every 2 seconds. It generates realistic 5G NR signal drift, crowd flow patterns, and security alerts.
2.  **WebSocket Broadcast**: Every update is broadcasted as a JSON payload to all connected dashboard clients.
3.  **Live Frontend Updates**: The `index.html` frontend receives the JSON data and surgically updates the DOM elements.
4.  **Resilient Connection**: The dashboard features an "Automatic Reconnect" system. If the backend goes down, it switches to a **Demo Mode** (simulated frontend data) and keeps trying to reconnect in the background.

---

## 🏃 Quick Start

### Prerequisites
- Python 3.9+
- pip (Python package manager)

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/MrDezire/5G_smart_stadium_experirnce_dashboard.git
   cd 5G_smart_stadium_experirnce_dashboard
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server**:
   ```bash
   python main.py
   ```
   *(Or use: `uvicorn main:app --host 0.0.0.0 --port 8000`)

4. **View the Dashboard**:
   Open your browser and navigate to `http://localhost:8000`.

---

## 🎨 Theme & Design
- **Primary Colors**: Deep Crimson (#C8102E) and Gold (#FFD700).
- **Aesthetic**: Modern glassmorphism with `backdrop-filter: blur`, neon glows, and depth-based scroll animations.
- **Typography**: Optimized for data density and operational clarity.

---

## 📂 Project Structure
- `main.py`: FastAPI server, WebSocket logic, and stadium data simulator.
- `index.html`: The complete single-page dashboard with responsive layout and live JS integration.
- `requirements.txt`: Project dependencies.
- `README.md`: Project documentation.

Created with ❤️ for the 5G Smart Stadium Experience.
