import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os
from dotenv import load_dotenv

# 1. Page Configuration
st.set_page_config(page_title="Emirates Airport Services | Manpower Optimizer", layout="wide", page_icon="✈️")

# 2. Load Model Artifacts
@st.cache_resource # Caches the model so it doesn't reload on every slider move
def load_assets():
    model = joblib.load('emirates_delay_model.pkl')
    features = joblib.load('model_features.pkl')
    return model, features

model, model_features = load_assets()

# 3. Sidebar - Input Parameters (Scenario Modeling)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/d/d0/Emirates_logo.svg", width=100)
st.sidebar.title("Operational Controls")
st.sidebar.markdown("Adjust parameters to simulate airport ground scenarios.")

st.sidebar.subheader("✈️ Flight Details")
ac_type = st.sidebar.selectbox("Aircraft Type", ["A380", "B777", "A320"])
arrival_hour = st.sidebar.slider("Arrival Hour (24h format)", 0, 23, 12)

st.sidebar.subheader("👷 Manpower Allocation")
staff_deployed = st.sidebar.number_input("Ramp Agents Deployed", min_value=1, max_value=40, value=15)

# 4. Logic: Prepare Model Input
# Identify peak wave (DXB Hub waves: 22-02, 07-09)
is_peak = 1 if arrival_hour in [22, 23, 0, 1, 2, 7, 8, 9] else 0

# Define Emirates Standard Requirements
req_map = {"A380": 20, "B777": 12, "A320": 6}
required = req_map[ac_type]
staff_gap = staff_deployed - required

# Create a DataFrame for prediction matching the one-hot encoded structure
input_df = pd.DataFrame(columns=model_features)
input_df.loc[0] = 0  # Fill with zeros
input_df['hour'] = arrival_hour
input_df['is_peak_wave'] = is_peak
input_df['actual_staff_deployed'] = staff_deployed
input_df['staff_gap'] = staff_gap
input_df[f'aircraft_type_{ac_type}'] = 1

# 5. Prediction Engine
prediction = model.predict(input_df)[0]
prediction = max(0, prediction) # Delays can't be negative

# 6. Main Dashboard UI
st.title("Manpower & Turnaround Forecaster")
st.markdown(f"**Current Scenario:** {ac_type} arriving at {arrival_hour}:00 with {staff_deployed} staff.")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Predicted Delay", f"{round(prediction, 1)} min", delta=f"{round(prediction, 1)} min", delta_color="inverse")

with col2:
    st.metric("Staffing Gap", f"{staff_gap}", delta=staff_gap, delta_color="normal")

with col3:
    status = "Optimal" if prediction < 5 else "At Risk" if prediction < 15 else "Critical"
    st.write(f"**Operational Status:**")
    if status == "Optimal": st.success(status)
    elif status == "At Risk": st.warning(status)
    else: st.error(status)

st.divider()

# 7. Business Insights Section
st.subheader("💡 Strategic Recommendations")
if staff_gap < 0:
    st.info(f"The {ac_type} usually requires {required} staff. You are currently understaffed by {abs(staff_gap)}.")
    st.write(f"Recommendation: Reallocate {abs(staff_gap)} agents from the 'Above the Wing' team to reduce the {round(prediction)} min delay.")
else:
    st.write(f"Resource utilization is high. Consider if these extra {staff_gap} agents are needed elsewhere in the terminal.")



