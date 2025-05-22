import json
import joblib
import csv
from kafka import KafkaConsumer
from datetime import datetime

# Wczytaj model
model = joblib.load("model.pkl")

# Inicjalizacja Kafka Consumer
consumer = KafkaConsumer(
    'sensor_stream',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='ml-consumer-log'
)

# Otwarzenie pliku CSV do zapisu alertów
with open("alerts.csv", mode="w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "machine_id", "probability"])

    print("✅ Konsument z logowaniem uruchomiony...\n")

    for message in consumer:
        data = message.value

        features = [[
            data["air_temperature"],
            data["process_temperature"],
            data["rotational_speed"],
            data["torque"],
            data["tool_wear"]
        ]]

        prob = model.predict_proba(features)[0][1]
        prob_rounded = round(prob, 3)

        if prob >= 0.3:
            print(f"🚨 ALERT | {data['machine_id']} | P = {prob_rounded}")
            writer.writerow([data["timestamp"], data["machine_id"], prob_rounded])
            file.flush()
        else:
            print(f"✅ OK    | {data['machine_id']} | P = {prob_rounded}")
