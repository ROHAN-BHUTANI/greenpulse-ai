import streamlit as st
import pandas as pd
import time
import os

st.set_page_config(layout="wide")

st.title("🌱 GreenPulse AI")
st.caption("Hack For Green Bharat | Real-Time Urban Environmental Intelligence (Powered by Pathway)")

csv_path = "greenpulse-pathway/live_output.csv"

# -----------------------------
# CHECK ENGINE STATUS
# -----------------------------

if not os.path.exists(csv_path):
    st.error("⚠ Pathway engine not running. Start engine.py inside WSL.")
    st.stop()

# -----------------------------
# READ STREAMING DATA
# -----------------------------

try:
    df = pd.read_csv(csv_path)

    if len(df) == 0:
        st.warning("Waiting for streaming data...")
        st.stop()

    latest = df.iloc[-1]

    st.markdown("## 📡 Live Environmental Metrics")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("AQI", int(latest["AQI"]))
    col2.metric("CO2 (ppm)", round(latest["CO2"], 2))
    col3.metric("Temperature (°C)", round(latest["temperature"], 2))
    col4.metric("Traffic Density", round(latest["traffic_density"], 2))
    col5.metric("Risk Score", round(latest["risk_score"], 2))

    st.line_chart(df[["AQI", "CO2", "temperature", "risk_score"]])

    st.markdown("## 🚨 Alert Status")

    alert = latest["alert"]

    if alert == "Severe Environmental Risk":
        st.error(alert)
    elif alert == "Moderate Environmental Risk":
        st.warning(alert)
    else:
        st.success("All environmental parameters within safe range.")

except Exception as e:
    st.error(f"Error reading data: {e}")
    st.stop()

# -----------------------------
# CHATBOT INTELLIGENCE LAYER
# -----------------------------

st.markdown("## 🤖 Sustainability Copilot")

user_question = st.text_input("Ask about AQI, risk trends, traffic impact, mitigation steps, or predictions")

def chatbot_response(question, df):
    question = question.lower()
    latest = df.iloc[-1]
    response = []

    # AQI related
    if "aqi" in question or "air" in question:
        if latest["AQI"] > 150:
            response.append("Current AQI indicates unhealthy air quality.")
            response.append("Outdoor exposure should be limited.")
        elif latest["AQI"] > 100:
            response.append("Air quality is moderate.")
            response.append("Sensitive groups should take precautions.")
        else:
            response.append("Air quality is within safe range.")

    # Risk
    elif "risk" in question:
        response.append(f"Current environmental risk score is {round(latest['risk_score'],2)}.")
        if latest["risk_score"] > 75:
            response.append("The city is under severe environmental stress.")
        elif latest["risk_score"] > 50:
            response.append("Risk levels are elevated but manageable.")
        else:
            response.append("Risk levels are stable.")

    # Traffic
    elif "traffic" in question:
        response.append(f"Traffic density is {round(latest['traffic_density'],2)}.")
        if latest["traffic_density"] > 70:
            response.append("High traffic likely contributing to emissions.")
            response.append("Congestion control measures recommended.")
        else:
            response.append("Traffic levels are moderate.")

    # Trend
    elif "trend" in question or "increasing" in question or "decreasing" in question:
        if len(df) > 5:
            trend = df["risk_score"].iloc[-1] - df["risk_score"].iloc[-5]
            if trend > 5:
                response.append("Environmental risk trend is increasing.")
            elif trend < -5:
                response.append("Environmental risk trend is decreasing.")
            else:
                response.append("Risk trend is stable.")
        else:
            response.append("Not enough historical data to compute trend.")

    # Prediction
    elif "predict" in question or "future" in question:
        projected = latest["risk_score"] * 1.05
        response.append(f"Projected short-term risk score: {round(projected,2)}.")
        if projected > 75:
            response.append("Conditions may escalate if no intervention occurs.")
        else:
            response.append("Situation likely to remain stable.")

    # Mitigation
    elif "mitigation" in question or "solution" in question or "improve" in question:
        response.append("Recommended mitigation strategies:")
        response.append("- Improve traffic flow management")
        response.append("- Promote public transportation")
        response.append("- Increase green urban zones")
        response.append("- Implement emission monitoring policies")

    else:
        response.append("I can help analyze AQI, risk trends, traffic impact, predictions, or mitigation strategies.")

    return "\n\n".join(response)


if st.button("Ask Copilot"):
    if user_question.strip() == "":
        st.warning("Please enter a question.")
    else:
        answer = chatbot_response(user_question, df)
        st.success(answer)

# -----------------------------
# AUTO REFRESH
# -----------------------------

time.sleep(2)
st.rerun()