import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Alerty Maszyn", layout="wide")

st.title("📊 Monitoring Awarii Maszyn w Czasie Rzeczywistym")

# Auto-refresh co 5 sekund
REFRESH_INTERVAL = 5  # sekund

def load_data():
    try:
        df = pd.read_csv("alerts.csv")
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp", ascending=False)
        return df
    except Exception:
        return pd.DataFrame(columns=["timestamp", "machine_id", "probability"])

placeholder = st.empty()

while True:
    with placeholder.container():
        df_alerts = load_data()
        if df_alerts.empty:
            st.warning("Brak alertów do wyświetlenia.")
        else:
            st.metric("🔔 Liczba alertów", len(df_alerts))
            st.dataframe(df_alerts, use_container_width=True)

    time.sleep(REFRESH_INTERVAL)
