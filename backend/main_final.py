from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import random
from datetime import datetime, timedelta
import uvicorn
import asyncio
import numpy as np

app = FastAPI(title="Intelligent Traffic Control System")

# Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data for traffic junctions
TRAFFIC_JUNCTIONS = [
    {"id": "J001", "name": "Main St & 1st Ave", "type": "intersection", "lat": 40.7128, "lon": -74.0060, "capacity": 200},
    {"id": "J002", "name": "2nd Ave & Broadway", "type": "intersection", "lat": 40.7580, "lon": -73.9855, "capacity": 300},
    {"id": "J003", "name": "5th Ave & 34th St", "type": "intersection", "lat": 40.7489, "lon": -73.9840, "capacity": 200},
    {"id": "J004", "name": "Times Square", "type": "intersection", "lat": 40.7580, "lon": -73.9855, "capacity": 400},
    {"id": "J005", "name": "Central Park West", "type": "roundabout", "lat": 40.7680, "lon": -73.9815, "capacity": 150},
]

class TrafficController:
    """Simple traffic controller without GNN dependencies"""
    
    @staticmethod
    def simulate_yolo_detection():
        """Simulate YOLOv8 vehicle detection"""
        detections = {}
        current_hour = datetime.now().hour
        
        for junction in TRAFFIC_JUNCTIONS:
            # Simulate traffic patterns based on time of day
            if 7 <= current_hour <= 9 or 16 <= current_hour <= 18:  # Rush hour
                base_vehicles = junction["capacity"] * 0.6
            elif 10 <= current_hour <= 15:  # Day time
                base_vehicles = junction["capacity"] * 0.4
            else:  # Night time
                base_vehicles = junction["capacity"] * 0.2
            
            # Add randomness
            vehicles = int(base_vehicles * random.uniform(0.7, 1.3))
            vehicles = min(vehicles, junction["capacity"])
            
            # Vehicle type distribution (simulating YOLO output)
            vehicle_types = {
                "car": int(vehicles * 0.6),
                "motorcycle": int(vehicles * 0.1),
                "bus": int(vehicles * 0.05),
                "truck": int(vehicles * 0.15),
                "emergency": int(vehicles * 0.02),
                "bicycle": int(vehicles * 0.08)
            }
            
            detections[junction["id"]] = {
                "junction_id": junction["id"],
                "name": junction["name"],
                "vehicles": vehicles,
                "pedestrians": int(vehicles * 0.15 * random.uniform(0.5, 1.5)),
                "congestion": vehicles / junction["capacity"],
                "vehicle_types": vehicle_types,
                "timestamp": datetime.now().isoformat(),
                "detection_confidence": round(random.uniform(0.85, 0.98), 2)
            }
        
        return detections
    
    @staticmethod
    def optimize_signals(detections):
        """Rule-based signal optimization (simplified without GNN)"""
        recommendations = []
        
        for junction in TRAFFIC_JUNCTIONS:
            data = detections.get(junction["id"], {})
            congestion = data.get("congestion", 0)
            
            # Simple intelligent rules based on congestion
            if congestion > 0.7:  # High congestion
                phases = [40, 20, 15, 25]  # Priority to main road
                action = "🚨 High Traffic: Extend main road green time by 25%"
            elif congestion > 0.4:  # Medium congestion
                phases = [30, 30, 20, 20]  # Balanced timing
                action = "⚠️ Medium Traffic: Maintain balanced signal timing"
            else:  # Low congestion
                phases = [25, 25, 25, 25]  # Equal phases
                action = "✅ Low Traffic: Optimize for pedestrian crossing"
            
            # Add slight randomness to simulate adaptive control
            phases = [p * random.uniform(0.95, 1.05) for p in phases]
            
            recommendations.append({
                "junction_id": junction["id"],
                "junction_name": junction["name"],
                "current_congestion": round(congestion, 3),
                "predicted_congestion": round(congestion * random.uniform(0.9, 1.1), 3),
                "phase_durations": [round(p, 1) for p in phases],
                "total_cycle_time": round(sum(phases), 1),
                "recommended_action": action,
                "optimization_score": round(random.uniform(0.7, 0.95), 2),
                "timestamp": datetime.now().isoformat()
            })
        
        return recommendations

# Initialize controller
controller = TrafficController()

# WebSocket for real-time updates
class ConnectionManager:
    def __init__(self):
        self.active_connections = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                self.disconnect(connection)

manager = ConnectionManager()

# ============ API ENDPOINTS ============

@app.get("/")
def root():
    return {
        "message": "🚦 Intelligent Traffic Control System API",
        "version": "1.0.0",
        "description": "YOLOv8 + Adaptive Signal Control",
        "endpoints": [
            "/docs - Interactive API documentation",
            "/api/detections - Real-time vehicle detections",
            "/api/signals - Optimized signal timings",
            "/api/junctions - Traffic junction information",
            "/ws - WebSocket for live updates"
        ]
    }

@app.get("/api/detections")
def get_detections():
    """Get current vehicle and pedestrian detections"""
    detections = controller.simulate_yolo_detection()
    
    # Calculate statistics
    total_vehicles = sum(d["vehicles"] for d in detections.values())
    avg_congestion = np.mean([d["congestion"] for d in detections.values()])
    
    return {
        "system": "YOLOv8 Detection System",
        "timestamp": datetime.now().isoformat(),
        "statistics": {
            "total_junctions": len(detections),
            "total_vehicles": total_vehicles,
            "average_congestion": round(avg_congestion, 3),
            "detection_accuracy": round(random.uniform(0.88, 0.96), 2)
        },
        "detections": detections
    }

@app.get("/api/signals")
def get_signals():
    """Get optimized traffic signal timings"""
    detections = controller.simulate_yolo_detection()
    recommendations = controller.optimize_signals(detections)
    
    # Network-wide metrics
    avg_congestion = np.mean([r["current_congestion"] for r in recommendations])
    efficiency = round((1 - avg_congestion) * 100, 1)
    
    return {
        "system": "Adaptive Signal Control System",
        "timestamp": datetime.now().isoformat(),
        "network_metrics": {
            "average_congestion": round(avg_congestion, 3),
            "network_efficiency": f"{efficiency}%",
            "total_signals_optimized": len(recommendations),
            "predicted_wait_time_reduction": f"{random.randint(15, 40)}%"
        },
        "recommendations": recommendations
    }

@app.get("/api/junctions")
def get_junctions():
    """Get all traffic junction information"""
    return {
        "junctions": TRAFFIC_JUNCTIONS,
        "road_network": [
            {"id": "R001", "source": "J001", "target": "J002", "length_km": 0.5, "lanes": 2, "type": "arterial"},
            {"id": "R002", "source": "J002", "target": "J003", "length_km": 0.8, "lanes": 3, "type": "arterial"},
            {"id": "R003", "source": "J003", "target": "J004", "length_km": 0.3, "lanes": 2, "type": "collector"},
            {"id": "R004", "source": "J004", "target": "J005", "length_km": 1.2, "lanes": 4, "type": "arterial"},
            {"id": "R005", "source": "J001", "target": "J005", "length_km": 1.5, "lanes": 2, "type": "local"},
        ],
        "network_stats": {
            "total_junctions": len(TRAFFIC_JUNCTIONS),
            "total_roads": 5,
            "average_capacity": int(np.mean([j["capacity"] for j in TRAFFIC_JUNCTIONS]))
        }
    }

@app.get("/api/analytics")
def get_analytics(hours: int = 24):
    """Get traffic analytics"""
    # Simulate historical data
    historical_data = []
    base_time = datetime.now() - timedelta(hours=hours)
    
    for i in range(min(hours * 4, 100)):  # Limit to 100 data points
        timestamp = base_time + timedelta(minutes=i * 15)
        for junction in TRAFFIC_JUNCTIONS:
            vehicles = int(junction["capacity"] * random.uniform(0.2, 0.8))
            historical_data.append({
                "timestamp": timestamp.isoformat(),
                "junction_id": junction["id"],
                "vehicles": vehicles,
                "congestion": vehicles / junction["capacity"],
                "speed": random.uniform(20, 60)
            })
    
    return {
        "analytics_period_hours": hours,
        "data_points": len(historical_data),
        "trend": "increasing" if random.random() > 0.5 else "decreasing",
        "peak_hour": random.randint(8, 18),
        "data": historical_data[:50]  # Return first 50 points
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time traffic updates"""
    await manager.connect(websocket)
    
    try:
        # Send initial state
        detections = controller.simulate_yolo_detection()
        signals = controller.optimize_signals(detections)
        
        await websocket.send_json({
            "type": "system_ready",
            "message": "🚦 Traffic Control System Connected",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "yolo_detection": "active",
                "signal_control": "active",
                "data_stream": "active"
            }
        })
        
        # Continuous updates
        update_count = 0
        while True:
            update_count += 1
            
            # Generate new data
            detections = controller.simulate_yolo_detection()
            signals = controller.optimize_signals(detections)
            
            # Calculate metrics
            total_vehicles = sum(d["vehicles"] for d in detections.values())
            avg_congestion = np.mean([d["congestion"] for d in detections.values()])
            
            # Send update
            await websocket.send_json({
                "type": "traffic_update",
                "update_id": update_count,
                "timestamp": datetime.now().isoformat(),
                "metrics": {
                    "total_vehicles": total_vehicles,
                    "average_congestion": round(avg_congestion, 3),
                    "junctions_monitored": len(detections),
                    "update_frequency": "3 seconds"
                },
                "detections": detections,
                "signals": signals
            })
            
            # Wait 3 seconds before next update
            await asyncio.sleep(3)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 INTELLIGENT TRAFFIC CONTROL SYSTEM")
    print("=" * 60)
    print("✅ YOLOv8 Detection: Simulated")
    print("✅ Adaptive Signal Control: Active")
    print("✅ Real-time WebSocket: Enabled")
    print("✅ Dashboard: http://localhost:3000")
    print("✅ API Server: http://localhost:8000")
    print("✅ API Documentation: http://localhost:8000/docs")
    print("=" * 60)
    
    uvicorn.run(
        "main_final:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )