import streamlit as st
import threading
import pandas as pd
from pipeline import run_stream, data_store
from rag_agent import ask_agent
import time

st.set_page_config(layout="wide")

st.title("🌱 GreenPulse AI")
st.caption("Hack For Green Bharat | Real-Time Urban Environmental Intelligence")

# Start streaming once
if "stream_started" not in st.session_state:
    thread = threading.Thread(target=run_stream, daemon=True)
    thread.start()
    st.session_state.stream_started = True

st.markdown("## 📡 Live Environmental Metrics")

if data_store:
    df = pd.DataFrame(data_store[-20:])

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("AQI", df.iloc[-1]["AQI"])
    col2.metric("CO2 (ppm)", df.iloc[-1]["CO2"])
    col3.metric("Temperature (°C)", df.iloc[-1]["temperature"])
    col4.metric("Traffic Density", df.iloc[-1]["traffic_density"])
    col5.metric("Risk Score", df.iloc[-1]["risk_score"])

    st.line_chart(df[["AQI", "CO2", "temperature", "risk_score"]])

    st.markdown("## 🚨 Alert Status")

    alert = df.iloc[-1]["alert"]

    if alert != "Normal":
        st.error(alert)
    else:
        st.success("All environmental parameters within safe range.")

    risk = df.iloc[-1]["risk_score"]

    if risk > 75:
        st.error("🔴 Severe Environmental Risk")
    elif risk > 50:
        st.warning("🟠 Moderate Environmental Risk")
    else:
        st.success("🟢 Low Environmental Risk")

    # Trend Detection (Fixed indentation)
    if len(df) > 5:
        trend = df["risk_score"].iloc[-1] - df["risk_score"].iloc[-5]

        if trend > 5:
            st.warning("📈 Risk trend increasing.")
        elif trend < -5:
            st.success("📉 Risk trend decreasing.")
        else:
            st.info("➡️ Risk trend stable.")

st.markdown("## 🤖 Sustainability Copilot")

question = st.text_input("Ask about current environmental conditions")

if st.button("Generate Analysis"):
    if question and data_store:
        latest_data = df.iloc[-1].to_dict()
        answer = ask_agent(question, latest_data)
        st.write(answer)

time.sleep(2)
st.rerun()
