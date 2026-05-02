"""
Smart Stadium 5G War Room — FastAPI Backend
Serves index.html + WebSocket real-time 5G metrics + REST endpoints.
Run: uvicorn main:app --host 0.0.0.0 --port 8000
"""

import asyncio
import json
import math
import os
import random
import time
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI(title="5G Stadium War Room")

START_TIME = time.time()

# ── State ────────────────────────────────────────────────────────────────
state = {
    "latency_ms": 0.8,
    "bandwidth_gbps": 4.2,
    "devices_connected": 12847,
    "embb_load_pct": 73,
    "urllc_load_pct": 45,
    "mmtc_load_pct": 88,
    "spectral_efficiency": 6.4,
    "beamforming_active": True,
    "frequency_band": "n78",
    "crowd_sections": [87, 72, 91, 65, 55, 80, 93, 70],
    "alerts": ["Gate 3 surge detected", "Camera 7 offline"],
    "ar_vr_users": 3240,
    "merch_sales": 234810,
    "edge_compute_load_pct": 65,
    "handover_success_pct": 99.8,
    "active_mmwave_beams": 185,
    "timestamp": "",
}

ALERT_POOL = [
    "Gate 3 surge detected",
    "Camera 7 offline",
    "Unattended bag at Section D",
    "VIP zone perimeter breach attempt",
    "Camera 2 rebooting",
    "Gate 5 crowd density spike",
    "Suspicious loitering near Gate 1",
    "Camera 4 feed restored",
    "Emergency exit C blocked",
    "Fire alarm test — Sector 6",
    "Unauthorized drone detected overhead",
    "Medical team dispatched to Stand B",
    "Gate 7 entry rate exceeding capacity",
    "Camera 9 night-mode activated",
    "Metal detector alert at Gate 2",
]

tick = 0


def evolve_state():
    """Advance simulation by one tick (~2 s)."""
    global tick
    tick += 1
    t = tick * 0.1

    # URLLC latency 0.4–1.2 ms
    state["latency_ms"] = round(0.8 + 0.4 * math.sin(t) + random.uniform(-0.05, 0.05), 2)
    state["latency_ms"] = max(0.4, min(1.2, state["latency_ms"]))

    # eMBB bandwidth 2–6 Gbps
    state["bandwidth_gbps"] = round(4.0 + 2.0 * math.sin(t * 0.7) + random.uniform(-0.3, 0.3), 1)
    state["bandwidth_gbps"] = max(2.0, min(6.0, state["bandwidth_gbps"]))

    # mMTC devices random-walk 12000–15000
    state["devices_connected"] += random.randint(-120, 150)
    state["devices_connected"] = max(12000, min(15000, state["devices_connected"]))

    # Slice loads
    state["embb_load_pct"] = max(30, min(95, state["embb_load_pct"] + random.randint(-3, 3)))
    state["urllc_load_pct"] = max(20, min(80, state["urllc_load_pct"] + random.randint(-2, 2)))
    state["mmtc_load_pct"] = max(50, min(99, state["mmtc_load_pct"] + random.randint(-2, 3)))

    # Spectral efficiency 4–8 bps/Hz
    state["spectral_efficiency"] = round(6.0 + 2.0 * math.sin(t * 0.5) + random.uniform(-0.2, 0.2), 1)
    state["spectral_efficiency"] = max(4.0, min(8.0, state["spectral_efficiency"]))

    # Beamforming mostly on
    state["beamforming_active"] = random.random() < 0.9

    # Crowd sections drift ±2, clamp 0–100
    state["crowd_sections"] = [
        max(0, min(100, s + random.randint(-2, 2))) for s in state["crowd_sections"]
    ]

    # Alerts — add new one every few ticks
    if tick % 3 == 0:
        new_alert = random.choice(ALERT_POOL)
        state["alerts"] = [new_alert] + state["alerts"][:9]

    # AR/VR users
    state["ar_vr_users"] += random.randint(-30, 50)
    state["ar_vr_users"] = max(2800, min(4500, state["ar_vr_users"]))

    # Merch sales increment
    state["merch_sales"] += random.randint(50, 500)

    # 5G extra metrics
    state["edge_compute_load_pct"] = max(40, min(95, state["edge_compute_load_pct"] + random.randint(-5, 5)))
    state["handover_success_pct"] = round(max(98.5, min(99.9, state["handover_success_pct"] + random.uniform(-0.1, 0.1))), 2)
    state["active_mmwave_beams"] = max(120, min(250, state["active_mmwave_beams"] + random.randint(-8, 8)))

    state["timestamp"] = datetime.now(timezone.utc).isoformat()


# ── WebSocket broadcast ──────────────────────────────────────────────────
clients: set[WebSocket] = set()


async def broadcast_loop():
    """Push updated metrics to all WebSocket clients every 2 s."""
    while True:
        evolve_state()
        payload = json.dumps(state)
        dead = set()
        for ws in clients:
            try:
                await ws.send_text(payload)
            except Exception:
                dead.add(ws)
        clients.difference_update(dead)
        await asyncio.sleep(2)


@app.on_event("startup")
async def startup():
    asyncio.create_task(broadcast_loop())


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            # Keep connection alive; ignore client messages
            await ws.receive_text()
    except WebSocketDisconnect:
        clients.discard(ws)


# ── REST endpoints ───────────────────────────────────────────────────────
@app.get("/api/5g-info")
async def fiveg_info():
    return JSONResponse(
        {
            "standard": "3GPP Release 16",
            "bands": ["n78 — 3.5 GHz Sub-6", "n258 — 26 GHz mmWave"],
            "peak_downlink_gbps": 10,
            "urllc_latency_target_ms": 1,
            "mmtc_device_density": "1 million/km²",
            "active_slices": 3,
            "beamforming": "64T64R Massive MIMO",
        }
    )


@app.get("/api/snapshot")
async def snapshot():
    return JSONResponse(state)


@app.get("/health")
async def health():
    return JSONResponse({"status": "ok", "uptime_seconds": round(time.time() - START_TIME, 1)})


# ── Serve frontend ──────────────────────────────────────────────────────
INDEX = Path(__file__).parent / "index.html"


@app.get("/")
async def root():
    return FileResponse(INDEX, media_type="text/html")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

