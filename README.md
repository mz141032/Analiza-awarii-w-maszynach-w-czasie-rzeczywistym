# 🛠️ Monitoring Awarii Maszyn – Projekt Real-Time Analytics

Projekt stworzony w ramach przedmiotu *Analiza danych w czasie rzeczywistym*.  
Celem jest wykrywanie potencjalnych awarii maszyn na podstawie danych strumieniowych oraz podejmowanie decyzji biznesowych w czasie rzeczywistym.

---

## 🎯 Cel biznesowy

System analizuje dane z czujników maszyn (temperatura, moment obrotowy, zużycie narzędzia, itd.) i przewiduje, czy istnieje ryzyko awarii.  
Jeśli prawdopodobieństwo awarii przekracza określony próg, generowany jest alert, który może być podstawą do:

- zatrzymania maszyny,
- wezwania serwisu,
- wysłania powiadomienia do operatora.

---

## 🧱 Architektura

System składa się z następujących komponentów:

- **Kafka + Zookeeper** – pośrednik danych (Docker)
- **Producer (`kafka_producer.py`)** – symuluje dane w czasie rzeczywistym (CSV → Kafka)
- **Model ML (`model.pkl`)** – klasyfikator Random Forest
- **Consumer (`kafka_consumer_ml_log.py`)** – odbiera dane, analizuje, zapisuje alerty
- **Dashboard (`alert_dashboard.py`)** – wizualizacja alertów na żywo (Streamlit)

---

## 📦 Pliki

| Plik                         | Opis                                           |
|-----------------------------|------------------------------------------------|
| `docker-compose.yml`        | Uruchamia Kafka i Zookeeper w Dockerze        |
| `train_model.py`            | Trenuje model ML i zapisuje `model.pkl`       |
| `kafka_producer.py`         | Wysyła dane z `simulation_data.csv` do Kafka |
| `kafka_consumer_ml_log.py`  | Przetwarza dane i zapisuje alerty             |
| `alert_dashboard.py`        | Dashboard w czasie rzeczywistym (Streamlit)   |
| `train_data.csv`            | Dane treningowe                               |
| `simulation_data.csv`       | Dane symulacyjne                              |
| `model.pkl`                 | Zapisany model Random Forest                  |

---

## 🚀 Uruchomienie krok po kroku

1. **Zbuduj i uruchom Kafka + Zookeeper**  
```bash
docker-compose up -d
```

2. **Utwórz topic Kafka**  
```bash
docker exec -it kafka /usr/bin/kafka-topics --create --topic sensor_stream --bootstrap-server localhost:9092
```

3. **(Opcjonalnie) Wytrenuj model ML**  
```bash
python train_model.py
```

4. **Uruchom producer (symulacja danych)**  
```bash
python kafka_producer.py
```

5. **Uruchom consumer z modelem ML**  
```bash
python kafka_consumer_ml_log.py
```

6. **Uruchom dashboard Streamlit**  
```bash
streamlit run alert_dashboard.py
```

---

## 🧠 Zastosowane technologie

- Python, Pandas, Scikit-learn
- Apache Kafka (`kafka-python`)
- Docker, Docker Compose
- Streamlit

---

## 📈 Możliwości rozbudowy

- Integracja z bazą danych
- Powiadomienia e-mail / SMS
- Lepszy UI dashboardu
- Wersja chmurowa (Kafka + ML w chmurze)
