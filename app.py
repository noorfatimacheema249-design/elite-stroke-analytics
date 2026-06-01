import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from engine import calculate_astral_probability, generate_synthetic_cohort
from reporter import generate_pdf_report

# Page Configuration for high-end feel
st.set_page_config(
    page_title="ASTRAL Stroke Predictive Analytics Engine",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Institutional CSS Injections (Hospital Theme)
st.markdown("""
    <style>
    /* Global Styles */
    .stApp { background-color: #FAFAFA; }
    h1, h2, h3 { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important; color: #0F172A !important; }
    
    /* Institutional Header Banner */
    .hospital-banner {
        background-color: #1E3A8A;
        padding: 24px;
        border-radius: 8px;
        color: #FFFFFF !important;
        margin-bottom: 24px;
        border-left: 6px solid #3B82F6;
    }
    .hospital-banner h1 { color: #FFFFFF !important; margin: 0; font-size: 2.2rem; font-weight: 600; letter-spacing: -0.5px; }
    .hospital-banner p { color: #93C5FD !important; margin: 4px 0 0 0; font-size: 1rem; }
    
    /* Section Containers */
    .clinical-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 16px;
    }
    
    /* Subheadings */
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1E293B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 16px;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 6px;
    }
    
    /* Executive Metric Display */
    .metric-box {
        background: #F8FAFC;
        border: 1px solid #CBD5E1;
        padding: 16px;
        border-radius: 6px;
        text-align: center;
    }
    .metric-val { font-size: 1.8rem; font-weight: 700; color: #1E3A8A; }
    .metric-lbl { font-size: 0.8rem; text-transform: uppercase; color: #64748B; font-weight: 600; margin-top: 4px; }
    </style>
""", unsafe_allow_html=True)

# Top Bar Header Design
st.markdown("""
    <div class="hospital-banner">
        <h1>Acute Ischemic Stroke Decision Support Architecture</h1>
        <p>Quantitative Risk Stratification Engine via Published Validation Parameters (ASTRAL Protocol)</p>
    </div>
""", unsafe_allow_html=True)

# Sleek Tabs
tab1, tab2 = st.tabs(["Patient Intake & Prognostic Analytics", "Population-Level Cohort Simulation Matrix"])

with tab1:
    col1, col2 = st.columns([1, 1.2], gap="large")
    
    with col1:
        st.markdown('<div class="clinical-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Clinical Demographics & Vitals</div>', unsafe_allow_html=True)
        
        patient_id = st.text_input("Patient Registry ID / EMR ID", value="PT-2026-8942")
        age = st.number_input("Patient Age (Years)", min_value=18, max_value=110, value=74)
        nihss = st.slider("Admission Neurological Deficit Severity Score (NIHSS)", 0, 42, 14)
        time_delay = st.number_input("Onset-to-Evaluation Delta (Hours)", min_value=0.1, max_value=24.0, value=3.5, step=0.5)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">Diagnostic Metrics</div>', unsafe_allow_html=True)
        
        visual_defect = st.checkbox("Acute Visual Field Defect Confirmed on Exam")
        impaired_loc = st.checkbox("Altered Level of Consciousness Present (NIHSS 1a > 0)")
        glucose = st.number_input("Admission Serum Glucose Level (mmol/L)", min_value=1.0, max_value=30.0, value=8.2, step=0.1)
        
        metrics = calculate_astral_probability(age, nihss, time_delay, visual_defect, glucose, impaired_loc)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="clinical-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Statistical Workspace & Outcome Forecast</div>', unsafe_allow_html=True)
        
        # Grid layout for technical metrics
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.markdown(f'<div class="metric-box"><div class="metric-val">{metrics["score"]}</div><div class="metric-lbl">ASTRAL Integer</div></div>', unsafe_allow_html=True)
        with m_col2:
            st.markdown(f'<div class="metric-box"><div class="metric-val">{metrics["probability"]*100:.1f}%</div><div class="metric-lbl">Unfavorable Outcome Risk</div></div>', unsafe_allow_html=True)
        with m_col3:
            st.markdown(f'<div class="metric-box"><div class="metric-val">[{metrics["ci_lower"]*100:.0f}%-{metrics["ci_upper"]*100:.0f}%]</div><div class="metric-lbl">95% Confidence Bounds</div></div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Clean Solid Corporate Gauge Chart
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = metrics['probability'] * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Probability of Unfavorable 3-Month Outcome (mRS 3-6)", 'font': {'size': 14, 'color': '#1E293B'}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
                'bar': {'color': "#1E3A8A"},
                'bgcolor': "#E2E8F0",
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 30], 'color': '#E2E8F0'},
                    {'range': [30, 70], 'color': '#CBD5E1'},
                    {'range': [70, 100], 'color': '#94A3B8'}
                ],
            }
        ))
        fig_gauge.update_layout(height=260, margin=dict(t=30, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Export Actions Block
        pdf_bytes = generate_pdf_report(patient_id, age, metrics)
        st.download_button(
            label="Download Clinical Brief PDF Document",
            data=pdf_bytes,
            file_name=f"Clinical_Prognosis_{patient_id}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="clinical-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Cohort Generation & Regression Scatter Matrix</div>', unsafe_allow_html=True)
    st.write("Model institutional sample datasets to trace risk distributions across multi-variable patient tracks.")
    
    cohort_size = st.slider("Select Dataset Simulation Sample Volume", 50, 500, 100)
    
    if st.button("Generate Synthetic Evaluation Cohort"):
        cohort_data = generate_synthetic_cohort(cohort_size)
        df = pd.DataFrame(cohort_data)
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Refined High-End Scatter Matrix Plot
        fig_scatter = px.scatter(
            df, 
            x="Age", 
            y="Unfavorable_Outcome_Risk", 
            size="Baseline_NIHSS", 
            color="ASTRAL_Score",
            labels={"Unfavorable_Outcome_Risk": "Outcome Probability Risk Margin (%)"},
            title="Biostatistical Breakdown: Age Matrix vs. Probability Vector (Node Area = NIHSS Variance)",
            color_continuous_scale=px.colors.sequential.Slate
        )
        fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

