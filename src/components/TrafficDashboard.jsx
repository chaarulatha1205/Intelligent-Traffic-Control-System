import React, { useState, useEffect } from 'react';
import './TrafficDashboard.css';

const TrafficDashboard = () => {
  const [trafficData, setTrafficData] = useState({
    totalVehicles: 0,
    avgCongestion: "0%",
    activeJunctions: 0,
    junctions: [],
    lastUpdate: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  });
  const [autoUpdate, setAutoUpdate] = useState(true);

  // Predefined junctions with realistic patterns
  const junctions = [
    { id: "J001", name: "Downtown Main St", baseCongestion: 0.7 },
    { id: "J002", name: "University Circle", baseCongestion: 0.5 },
    { id: "J003", name: "Industrial Park", baseCongestion: 0.3 },
    { id: "J004", name: "Residential North", baseCongestion: 0.4 },
    { id: "J005", name: "Shopping District", baseCongestion: 0.6 }
  ];

  const generateTrafficData = () => {
    const now = new Date();
    const hour = now.getHours();
    
    // Time-based traffic patterns
    let timeFactor;
    if ((hour >= 7 && hour <= 9) || (hour >= 16 && hour <= 18)) {
      timeFactor = 2.5; // Rush hour
    } else if (hour >= 10 && hour <= 15) {
      timeFactor = 1.5; // Daytime
    } else {
      timeFactor = 0.3; // Night
    }

    let totalVehicles = 0;
    let totalCongestion = 0;
    let activeJunctions = 0;
    const generatedJunctions = [];

    junctions.forEach(junction => {
      // Generate random vehicle count
      const baseCount = Math.floor(Math.random() * 30 + 20);
      const vehicleCount = Math.floor(baseCount * junction.baseCongestion * timeFactor * (0.8 + Math.random() * 0.4));
      
      // Calculate congestion (0-100%)
      const congestion = Math.min(100, Math.floor((vehicleCount / 60) * 100));
      
      // Determine signal state
      let signalState;
      let signalColor;
      if (congestion > 70) {
        signalState = "RED";
        signalColor = "#ef4444";
      } else if (congestion > 40) {
        signalState = "YELLOW";
        signalColor = "#f59e0b";
      } else {
        signalState = "GREEN";
        signalColor = "#10b981";
      }

      // Add to totals
      totalVehicles += vehicleCount;
      totalCongestion += congestion;
      if (vehicleCount > 5) activeJunctions++;

      generatedJunctions.push({
        ...junction,
        vehicles: vehicleCount,
        congestion: `${congestion}%`,
        signal: signalState,
        signalColor,
        lastUpdate: now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      });
    });

    return {
      totalVehicles,
      avgCongestion: `${Math.floor(totalCongestion / junctions.length)}%`,
      activeJunctions,
      junctions: generatedJunctions,
      lastUpdate: now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    };
  };

  const updateTrafficData = () => {
    const newData = generateTrafficData();
    setTrafficData(newData);
  };

  useEffect(() => {
    // Initial data
    updateTrafficData();

    // Auto-update every 10 seconds
    if (autoUpdate) {
      const interval = setInterval(updateTrafficData, 10000);
      return () => clearInterval(interval);
    }
  }, [autoUpdate]);

  const toggleAutoUpdate = () => {
    setAutoUpdate(!autoUpdate);
  };

  return (
    <div className="traffic-dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-top">
          <div className="system-title">
            <h1>🚦 Intelligent Traffic Control System</h1>
            <p>Real-time Adaptive Signal Control</p>
          </div>
          <div className="system-status">
            <div className="status-indicator">
              <span className="status-dot"></span>
              <span>SYSTEM ACTIVE</span>
            </div>
            <div className="status-indicator">
              <span>Last update: {trafficData.lastUpdate}</span>
            </div>
            <div className="status-indicator">
              <span>Auto-refresh: {autoUpdate ? "10 seconds" : "PAUSED"}</span>
            </div>
          </div>
        </div>

        {/* Metrics */}
        <div className="metrics-grid">
          <div className="metric-card">
            <h3>Total Vehicles</h3>
            <p className="metric-value">{trafficData.totalVehicles}</p>
          </div>
          <div className="metric-card">
            <h3>Avg Congestion</h3>
            <p className="metric-value">{trafficData.avgCongestion}</p>
          </div>
          <div className="metric-card">
            <h3>Active Junctions</h3>
            <p className="metric-value">{trafficData.activeJunctions}</p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="dashboard-main">
        <div className="section-header">
          <h2>Traffic Junctions</h2>
          <div className="auto-update-badge">
            Auto-update: {autoUpdate ? "10s" : "OFF"}
          </div>
        </div>

        {/* Junctions Grid */}
        <div className="junctions-grid">
          {trafficData.junctions.map((junction) => (
            <div key={junction.id} className="junction-card">
              <div className="junction-header">
                <h3>{junction.id}</h3>
                <span
                  className="signal-indicator"
                  style={{ backgroundColor: junction.signalColor }}
                ></span>
              </div>
              <p className="junction-name">{junction.name}</p>
              <div className="junction-metrics">
                <div className="metric">
                  <span className="metric-label">Vehicles</span>
                  <span className="metric-value">{junction.vehicles}</span>
                </div>
                <div className="metric">
                  <span className="metric-label">Congestion</span>
                  <span className="metric-value">{junction.congestion}</span>
                </div>
              </div>
              <div className="junction-footer">
                <span className="update-time">
                  Updated: {junction.lastUpdate}
                </span>
                <span
                  className="signal-state"
                  style={{ color: junction.signalColor }}
                >
                  Signal: {junction.signal}
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* Controls */}
        <div className="control-panel">
          <button onClick={updateTrafficData} className="btn btn-primary">
            Update Now
          </button>
          <button onClick={toggleAutoUpdate} className="btn btn-secondary">
            {autoUpdate ? "Pause Auto-Update" : "Resume Auto-Update"}
          </button>
        </div>
      </main>

      {/* Footer */}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: "20px",
          margin: "40px 0",
        }}
      >
        <div style={{ textAlign: "center", padding: "20px" }}>
          <div
            style={{
              fontSize: "40px",
              fontWeight: "bold",
              color: "#2563eb",
              marginBottom: "10px",
            }}
          >
            01
          </div>
          <div
            style={{
              fontSize: "18px",
              fontWeight: "bold",
              marginBottom: "5px",
            }}
          >
            CHAARULATHA J
          </div>
          <div style={{ fontSize: "14px", color: "#64748b" }}>
            System Architect
          </div>
        </div>

        <div style={{ textAlign: "center", padding: "20px" }}>
          <div
            style={{
              fontSize: "40px",
              fontWeight: "bold",
              color: "#2563eb",
              marginBottom: "10px",
            }}
          >
            02
          </div>
          <div
            style={{
              fontSize: "18px",
              fontWeight: "bold",
              marginBottom: "5px",
            }}
          >
            AKAASH M K
          </div>
          <div style={{ fontSize: "14px", color: "#64748b" }}>Data Analyst</div>
        </div>

        <div style={{ textAlign: "center", padding: "20px" }}>
          <div
            style={{
              fontSize: "40px",
              fontWeight: "bold",
              color: "#2563eb",
              marginBottom: "10px",
            }}
          >
            03
          </div>
          <div
            style={{
              fontSize: "18px",
              fontWeight: "bold",
              marginBottom: "5px",
            }}
          >
            E. THEERTHA
          </div>
          <div style={{ fontSize: "14px", color: "#64748b" }}>
            Frontend Developer
          </div>
        </div>

        <div style={{ textAlign: "center", padding: "20px" }}>
          <div
            style={{
              fontSize: "40px",
              fontWeight: "bold",
              color: "#2563eb",
              marginBottom: "10px",
            }}
          >
            04
          </div>
          <div
            style={{
              fontSize: "18px",
              fontWeight: "bold",
              marginBottom: "5px",
            }}
          >
            VINYTHA S V
          </div>
          <div style={{ fontSize: "14px", color: "#64748b" }}>
            UI/UX Designer
          </div>
        </div>
      </div>

      <footer className="dashboard-footer">
        Intelligent Adaptive Signal Control System | Mock Data Simulation | For
        Demonstration Purposes
      </footer>
    </div>
  );
};

export default TrafficDashboard;