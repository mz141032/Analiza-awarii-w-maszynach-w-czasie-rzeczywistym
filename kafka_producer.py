import pandas as pd
import json
import time
from kafka import KafkaProducer
from datetime import datetime

# Wczytanie danych z pliku CSV 
df = pd.read_csv("simulation_data.csv")

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for _, row in df.iterrows():
    message = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "machine_id": row["machine_id"],
        "air_temperature": row["Air temperature [K]"],
        "process_temperature": row["Process temperature [K]"],
        "rotational_speed": int(row["Rotational speed [rpm]"]),
        "torque": row["Torque [Nm]"],
        "tool_wear": int(row["Tool wear [min]"]),
    }
    producer.send("sensor_stream", message)
    print("Wysłano:", message)
    time.sleep(1)

producer.flush()
producer.close()
