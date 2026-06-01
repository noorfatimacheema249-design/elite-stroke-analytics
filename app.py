import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from engine import calculate_astral_probability, generate_synthetic_cohort
from reporter import generate_pdf_report

st.set_page_config(
    page_title="Stroke Predictive Analytics Engine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header { font-size:2.4rem !important; color: #1A365D; font-weight: 700; }
    .sub-text { font-size:1.1rem; color: #4A5568; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🧠 Acute Stroke Clinical Decision Support Suite</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Advanced Predictive Modeling & Analytics for 3-Month Functional Outcomes (ASTRAL Protocol)</p>', unsafe_allow_html=True)
st.divider()

tab1, tab2 = st.tabs(["🎯 Individual Patient Analytics", "📊 Cohort Simulation Studio"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Admission Parameters")
        patient_id = st.text_input("Patient Registry ID", value="PT-2026-8942")
        age = st.number_input("Patient Age (Years)", min_value=18, max_value=110, value=74)
        nihss = st.slider("Baseline NIHSS Score (Severity)", 0, 42, 14)
        time_delay = st.number_input("Onset-to-Door Delta (Hours)", min_value=0.1, max_value=24.0, value=3.5, step=0.5)
        
        st.markdown("**Neurological Deficits**")
        visual_defect = st.checkbox("Acute Visual Field Defect Presence")
        impaired_loc = st.checkbox("Depressed Level of Consciousness (NIHSS 1a > 0)")
        
        st.markdown("**Metabolic Profile**")
        glucose = st.number_input("Admission Serum Glucose (mmol/L)", min_value=1.0, max_value=30.0, value=8.2, step=0.1)
        
        metrics = calculate_astral_probability(age, nihss, time_delay, visual_defect, glucose, impaired_loc)
        
    with col2:
        st.subheader("📊 Predictive Probability Workspace")
        
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("ASTRAL Integer Score", f"{metrics['score']} Pts")
        m_col2.metric("Predicted Unfavorable Risk", f"{metrics['probability']*100:.1f}%")
        m_col3.metric("95% Confidence Interval", f"[{metrics['ci_lower']*100:.0f}% - {metrics['ci_upper']*100:.0f}%]")
        
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = metrics['probability'] * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "3-Month Poor Outcome Risk (mRS 3-6)", 'font': {'size': 16}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#1A365D"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 30], 'color': '#C6F6D5'},
                    {'range': [30, 70], 'color': '#FEFCBF'},
                    {'range': [70, 100], 'color': '#FED7D7'}
                ],
            }
        ))
        fig_gauge.update_layout(height=280, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        pdf_bytes = generate_pdf_report(patient_id, age, metrics)
        st.download_button(
            label="📥 Export Certified Clinical PDF Brief",
            data=pdf_bytes,
            file_name=f"Stroke_Brief_{patient_id}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

with tab2:
    st.subheader("📈 Population-Level Cohort Risk Modeling")
    st.write("Simulate a custom validation cohort to evaluate system performance metrics dynamically across changing sample sizes.")
    
    cohort_size = st.slider("Select Simulation Sample Volume", 50, 500, 100)
    
    if st.button("Generate Synthetic Clinical Cohort"):
        cohort_data = generate_synthetic_cohort(cohort_size)
        df = pd.DataFrame(cohort_data)
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("**Risk Distribution Cross-Analysis**")
        fig_scatter = px.scatter(
            df, 
            x="Age", 
            y="Unfavorable_Outcome_Risk", 
            size="Baseline_NIHSS", 
            color="ASTRAL_Score",
            labels={"Unfavorable_Outcome_Risk": "Predicted Risk (%)"},
            title="Correlation Matrix: Age vs. Risk Magnitude (Point Size = NIHSS Severity)",
            color_continuous_scale=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
