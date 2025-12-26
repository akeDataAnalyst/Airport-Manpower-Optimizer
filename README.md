# Emirates Airport Services: Manpower & Turnaround Optimizer

## Executive Summary
In high-frequency airport operations, **Turnaround Time (TAT)** is a critical KPI. At major hubs like Dubai International (DXB), the "Below the Wing" operations (loading, fueling, catering) must be perfectly synchronized. 

This project addresses the **Manpower Forecasting** and **Scenario Modelling** requirements for the Data Analytics Officer role. I developed a predictive system that identifies potential ground delays before they happen by analyzing the gap between required and deployed ramp agents during peak hub "waves."

---

## The Tech Stack
* **Database:** MySQL (Relational storage for schedules and operational actuals).
* **Language:** Python (Pandas for ETL, Scikit-Learn for Predictive Modeling).
* **ML Model:** Random Forest Regressor (Selected for its ability to model non-linear operational bottlenecks).
* **Security:** `python-dotenv` (Enterprise-grade environment variable management).
* **Dashboard:** Streamlit (Interactive "What-If" simulation tool for Duty Managers).

---

## Project Architecture & Workflow


1.  **Data Engineering (SQL):** * Designed a relational schema in MySQL to house flight schedules and operational performance.
    * Created `v_manpower_gap_analysis` view to calculate real-time staffing variances based on aircraft complexity (A380 vs. B777 vs. A320).
2.  **Feature Engineering (Python):** * Extracted **Hub Peak Waves**: Categorized arrivals into DXB's midnight (22:00-02:00) and morning (07:00-09:00) waves.
    * Engineered the **Staffing Gap** feature to quantify the impact of under-allocation on departure punctuality.
3.  **Predictive Modeling:** * Trained a Random Forest model to predict turnaround delays in minutes.
    * **Result:** Achieved a Mean Absolute Error (MAE) of **13.68 minutes**, providing a baseline for identifying high-risk flights.
4.  **Operational Dashboard:** * Built a Streamlit application allowing users to adjust staffing levels and see the predicted impact on delays instantly.

---

## Operational Insights
* **Non-Linearity:** The model revealed that for wide-body aircraft (A380), the relationship between staff and delay is non-linear; missing the "minimum threshold" of 20 agents causes exponential delay growth.
* **Peak Sensitivity:** Flights arriving during "Peak Waves" are 3x more sensitive to staffing shortages due to shared ground equipment across gates.

---

## Future Roadmap
* **Incorporate Real-time Feeds:** Integrate FlightRadar24 API for live arrival tracking.
* **GSE Integration:** Factor in Ground Service Equipment (GSE) availability into the prediction model.
* **Refinement:** Introduce "Deep Learning" (LSTM) to account for time-series dependencies in gate availability.

---
**Developed by:** Aklilu Abera 
