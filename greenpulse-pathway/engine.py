import pathway as pw
import random
import time


# -----------------------------
# Schema
# -----------------------------

class EnvironmentalInput(pw.Schema):
    AQI: int
    CO2: float
    temperature: float
    traffic_density: float


# -----------------------------
# Streaming Connector
# -----------------------------

class EnvironmentalStream(pw.io.python.ConnectorSubject):

    def run(self):
        while True:
            self.next(
                AQI=random.randint(50, 250),
                CO2=random.uniform(350, 900),
                temperature=random.uniform(20, 45),
                traffic_density=random.uniform(0, 100),
            )
            time.sleep(2)


env_stream = pw.io.python.read(
    EnvironmentalStream(),
    schema=EnvironmentalInput,
)


# -----------------------------
# Risk Computation (Expression Safe)
# -----------------------------

processed = env_stream.with_columns(
    risk_score=(
        0.4 * pw.this.AQI
        + 0.02 * pw.this.CO2
        + 0.2 * pw.this.temperature
        + 0.2 * pw.this.traffic_density
    )
)

processed = processed.with_columns(
    risk_score=pw.if_else(
        pw.this.risk_score > 100,
        100,
        pw.this.risk_score
    )
)

processed = processed.with_columns(
    alert=pw.if_else(
        pw.this.risk_score > 75,
        "Severe Environmental Risk",
        pw.if_else(
            pw.this.risk_score > 50,
            "Moderate Environmental Risk",
            "Normal"
        )
    )
)


# -----------------------------
# CSV Output
# -----------------------------

pw.io.csv.write(
    processed,
    "live_output.csv"
)


# -----------------------------
# Run
# -----------------------------

if __name__ == "__main__":
    pw.run()
