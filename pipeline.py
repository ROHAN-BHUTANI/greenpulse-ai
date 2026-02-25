import random
import time
from datetime import datetime

data_store = []

def generate_data():
    return {
        "timestamp": datetime.now(),
        "AQI": random.randint(50, 400),
        "CO2": random.randint(300, 600),
        "temperature": random.randint(20, 45),
        "traffic_density": random.randint(10, 100),
    }

def calculate_risk_score(aqi, co2, temp, traffic):
    score = 0

    # Weighted scoring (0–100 scale)
    score += min(aqi / 4, 25)
    score += min(co2 / 20, 25)
    score += min(temp, 25)
    score += min(traffic / 4, 25)

    return round(score, 2)

def detect_alert(row):
    if row["AQI"] > 300 and row["traffic_density"] > 80:
        return "Urban Congestion Pollution Alert"
    elif row["CO2"] > 450:
        return "Industrial Emission Alert"
    elif row["temperature"] > 42:
        return "Heatwave Risk Alert"
    return "Normal"

def run_stream():
    while True:
        new_data = generate_data()

        new_data["risk_score"] = calculate_risk_score(
            new_data["AQI"],
            new_data["CO2"],
            new_data["temperature"],
            new_data["traffic_density"]
        )

        new_data["alert"] = detect_alert(new_data)

        data_store.append(new_data)

        # Keep last 100 records
        if len(data_store) > 100:
            data_store.pop(0)

        time.sleep(2)
