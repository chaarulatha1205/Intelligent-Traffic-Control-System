import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import random

# Generate junctions data
junctions_data = []
for i in range(15):
    junction = {
        "junction_id": f"J{i:03d}",
        "name": f"Intersection {i+1}",
        "type": random.choice(["intersection", "roundabout", "t-junction"]),
        "latitude": 40.7128 + (i // 5) * 0.01,
        "longitude": -74.0060 + (i % 5) * 0.01,
        "lanes": random.choice([2, 3, 4]),
        "capacity": random.randint(100, 300),
        "pedestrian_crossing": random.choice([True, False]),
        "bus_stop": random.choice([True, False])
    }
    junctions_data.append(junction)

# Generate roads data
roads_data = []
road_id = 0
for i in range(len(junctions_data)):
    for j in range(i+1, min(i+3, len(junctions_data))):
        roads_data.append({
            "road_id": f"R{road_id:04d}",
            "source_junction": junctions_data[i]["junction_id"],
            "target_junction": junctions_data[j]["junction_id"],
            "length_km": round(random.uniform(0.3, 1.5), 2),
            "lanes": random.choice([1, 2, 3]),
            "speed_limit": random.choice([30, 40, 50, 60]),
            "road_type": random.choice(["arterial", "collector", "local"])
        })
        road_id += 1

# Generate traffic time-series data
traffic_data = []
base_date = datetime(2024, 1, 1)

for day in range(7):  # 7 days
    for hour in range(24):
        for minute in [0, 15, 30, 45]:  # Every 15 minutes
            timestamp = base_date + timedelta(days=day, hours=hour, minutes=minute)
            
            for junction in junctions_data:
                # Rush hour pattern
                if 7 <= hour <= 9 or 16 <= hour <= 18:
                    base_traffic = junction["capacity"] * 0.7
                elif 10 <= hour <= 15:
                    base_traffic = junction["capacity"] * 0.4
                else:
                    base_traffic = junction["capacity"] * 0.2
                
                vehicles = int(base_traffic * random.uniform(0.8, 1.2))
                vehicles = min(vehicles, junction["capacity"])
                
                traffic_data.append({
                    "timestamp": timestamp.isoformat(),
                    "junction_id": junction["junction_id"],
                    "vehicles": vehicles,
                    "pedestrians": int(vehicles * 0.1 * random.uniform(0.5, 1.5)),
                    "congestion": vehicles / junction["capacity"],
                    "avg_speed": random.uniform(10, 60),
                    "incident": random.random() < 0.05  # 5% chance of incident
                })

# Save to files
pd.DataFrame(junctions_data).to_csv("datasets/junctions.csv", index=False)
pd.DataFrame(roads_data).to_csv("datasets/roads.csv", index=False)
pd.DataFrame(traffic_data).to_csv("datasets/traffic_timeseries.csv", index=False)

print("✅ Datasets generated successfully!")
print(f"  - Junctions: {len(junctions_data)} records")
print(f"  - Roads: {len(roads_data)} records")
print(f"  - Traffic data: {len(traffic_data)} records")