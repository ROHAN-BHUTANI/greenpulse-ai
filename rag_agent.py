def ask_agent(question, live_data):

    aqi = live_data["AQI"]
    co2 = live_data["CO2"]
    temp = live_data["temperature"]
    traffic = live_data["traffic_density"]
    risk = live_data["risk_score"]

    response = "Environmental Analysis Report\n\n"
    response += f"Current Risk Score: {risk}/100\n\n"

    # Environmental conditions
    if aqi > 300:
        response += "- AQI is in hazardous range.\n"
    if co2 > 450:
        response += "- CO2 levels indicate possible industrial emissions.\n"
    if temp > 42:
        response += "- Heatwave conditions detected.\n"
    if traffic > 80:
        response += "- High traffic density contributing to pollution.\n"

    # Risk classification
    if risk > 75:
        response += "\nSevere Environmental Risk Detected.\n"
    elif risk > 50:
        response += "\nModerate Environmental Risk Detected.\n"
    else:
        response += "\nEnvironmental conditions are stable.\n"

    response += "\nRecommended Actions:\n"

    if aqi > 300:
        response += "- Issue public health advisory.\n"
    if co2 > 450:
        response += "- Inspect nearby industrial facilities.\n"
    if traffic > 80:
        response += "- Implement traffic diversion strategy.\n"
    if temp > 42:
        response += "- Activate heatwave emergency protocols.\n"

    if (
        aqi <= 300
        and co2 <= 450
        and temp <= 42
        and traffic <= 80
    ):
        response += "- Continue monitoring environmental parameters.\n"

    return response
