import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from engine import calculate_astral_probability, generate_synthetic_cohort
from reporter import generate_pdf_report

# ---------------------------------------------------------
# Enterprise UX Configuration & Header Injection
# ---------------------------------------------------------
st.set_page_config(
    page_title="NeuroPro Analytics - Stroke Architecture Suite",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Total CSS Overhaul: Hides Streamlit branding, custom fonts, enterprise layouts
st.markdown("""
    <style>
    /* Import Premium Institutional Font Mapping */
    @import url('https://googleapis.com');
    
    /* Clean CSS Reset & Global Typography Overrides */
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background-color: #0F172A; color: #F1F5F9; }
    
    /* Hide Default Generic Streamlit Branding Hooks */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stHeader"] {background: rgba(0,0,0,0); height: 0rem;}
    
    /* Global Control Theme Customization */
    div[data-baseweb="input"] { background-color: #1E293B !important; border: 1px solid #334155 !important; border-radius: 6px !important; color: #F1F5F9 !important; }
    div[data-baseweb="select"] { background-color: #1E293B !important; border: 1px solid #334155 !important; border-radius: 6px !important; }
    .stSlider [data-testid="stMarkdownContainer"] { color: #94A3B8 !important; font-weight: 500; }
    
    /* Premium Institutional Application Header Control */
    .app-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: radial-gradient(100% 100% at 0% 0%, #1E3A8A 0%, #0F172A 100%);
        padding: 24px 40px;
        border-bottom: 1px solid #1E293B;
        margin: -60px -40px 32px -40px;
    }
    .brand-title { font-size: 1.6rem; font-weight: 700; color: #FFFFFF; letter-spacing: -0.03em; }
    .brand-subtitle { font-size: 0.85rem; color: #38BDF8; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 2px; }
    .system-status { font-size: 0.8rem; color: #10B981; background: rgba(16, 185, 129, 0.1); padding: 6px 12px; border-radius: 20px; border: 1px solid rgba(16, 185, 129, 0.2); font-weight: 500; }
    
    /* High-Fidelity Content Containers */
    .module-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .module-title { font-size: 1.05rem; font-weight: 600; color: #F8FAFC; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 24px; border-left: 4px solid #38BDF8; padding-left: 12px; }
    
    /* Corporate Executive Metric Scorecard Matrix */
    .metric-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 28px; }
    .metric-card { background: #0F172A; border: 1px solid #334155; border-radius: 8px; padding: 20px; text-align: center; }
    .metric-value { font-size: 2rem; font-weight: 700; color: #38BDF8; letter-spacing: -0.02em; }
    .metric-label { font-size: 0.75rem; text-transform: uppercase; color: #94A3B8; font-weight: 600; letter-spacing: 0.04em; margin-top: 6px; }
    
    /* Custom High-Fidelity Button Interface */
    .stDownloadButton button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    .stDownloadButton button:hover { transform: translateY(-1px); box-shadow: 0 6px 16px rgba(37, 99, 235, 0.3) !important; }
    
    /* Custom Dataframe Aesthetics */
    [data-testid="stDataFrame"] { background-color: #0F172A; border-radius: 8px; border: 1px solid #334155; }
    
    /* Streamlit Tab Custom Styling Rules */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: #0F172A; padding: 6px; border-radius: 8px; border: 1px solid #334155; }
    .stTabs [data-baseweb="tab"] { color: #94A3B8 !important; font-weight: 500 !important; padding: 10px 20px !important; border-radius: 6px !important; border: none !important; }
    .stTabs [aria-selected="true"] { background-color: #1E293B !important; color: #FFFFFF !important; font-weight: 600 !important; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Enterprise Application Top Bar Header Layout
# ---------------------------------------------------------
st.markdown("""
    <div class="app-header">
        <div>
            <div class="brand-title">NeuroPro Analytics Suite</div>
            <div class="brand-subtitle">Acute Ischemic Stroke Decision Architecture Engine</div>
        </div>
        <div class="system-status">Institutional Production Node Active</div>
    </div>
""", unsafe_allow_html=True)

# Application Workspaces Tabs
tab1, tab2 = st.tabs(["Clinical Diagnostics Workspace", "Cohort Simulation Matrix Laboratory"])

with tab1:
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.markdown('<div class="module-title">Patient Intake & Demographics</div>', unsafe_allow_html=True)
        
        patient_id = st.text_input("EMR Registry Identifier Link", value="EMR-2026-98412")
        age = st.number_input("Patient Baseline Age (Years)", min_value=18, max_value=110, value=74)
        nihss = st.slider("Admission Neurological Deficit Variance Metric (NIHSS Global Scale)", 0, 42, 14)
        time_delay = st.number_input("Estimated Symptom Onset-to-Evaluation Delta (Hours)", min_value=0.1, max_value=24.0, value=3.5, step=0.5)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.markdown('<div class="module-title">Biomarker & Clinical Status Matrix</div>', unsafe_allow_html=True)
        visual_defect = st.checkbox("Acute Cortical Visual Field Track Defect Presence")
        impaired_loc = st.checkbox("Depressed / Altered Consciousness Index Verified (NIHSS 1a > 0)")
        glucose = st.number_input("Verified Laboratory Admission Serum Glucose Volume (mmol/L)", min_value=1.0, max_value=30.0, value=8.2, step=0.1)
        
        metrics = calculate_astral_probability(age, nihss, time_delay, visual_defect, glucose, impaired_loc)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.markdown('<div class="module-title">Statistical Workspace & Forecast Yield</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-grid">
                <div class="metric-card"><div class="metric-value">{metrics["score"]}</div><div class="metric-label">ASTRAL Index</div></div>
                <div class="metric-card"><div class="metric-value">{metrics["probability"]*100:.1f}%</div><div class="metric-label">Poor Outcome Risk</div></div>
                <div class="metric-card"><div class="metric-value">[{metrics["ci_lower"]*100:.0f}%-{metrics["ci_upper"]*100:.0f}%]</div><div class="metric-label">95% Conf. Boundary</div></div>
            </div>
        """, unsafe_allow_html=True)
        
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = metrics['probability'] * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Mathematical Variance of Unfavorable 3-Month Outcome (mRS 3-6)", 'font': {'size': 13, 'color': '#94A3B8', 'family': 'Inter'}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569", 'tickfont': {'color': '#64748B', 'family': 'Inter'}},
                'bar': {'color': "#38BDF8"},
                'bgcolor': "#1E293B",
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 30], 'color': '#1E293B'},
                    {'range': [30, 70], 'color': '#111827'},
                    {'range': [70, 100], 'color': '#030712'}
                ],
            }
        ))
        fig_gauge.update_layout(
            height=240, 
            margin=dict(t=40, b=10, l=10, r=10), 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#FFFFFF', 'family': 'Inter'}
        )
        st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
        
        pdf_bytes = generate_pdf_report(patient_id, age, metrics)
        st.markdown("<div style='margin-top: 12px;'>", unsafe_allow_html=True)
        st.download_button(
            label="Compile & Authenticate Institutional Brief (PDF)",
            data=pdf_bytes,
            file_name=f"NeuroPro_Brief_{patient_id}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.markdown('<div class="module-title">Biostatistical Simulation Framework & Core Analytics</div>', unsafe_allow_html=True)
with tab2:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.markdown('<div class="module-title">Biostatistical Simulation Framework & Core Analytics</div>', unsafe_allow_html=True)
    st.write("Delineate mathematical regression weights across multi-variable verification pathways utilizing automated patient synthetic modeling pools.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    cohort_size = st.slider("Target Active Model Control Pipeline Sizing Data Volume", 50, 500, 100)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Initialize Pipeline Processing Execution Track"):
        cohort_data = generate_synthetic_cohort(cohort_size)
        df = pd.DataFrame(cohort_data)
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        fig_scatter = px.scatter(
            df, 
            x="Age", 
            y="Unfavorable_Outcome_Risk", 
            size="Baseline_NIHSS", 
            color="ASTRAL_Score",
            labels={"Unfavorable_Outcome_Risk": "Outcome Risk Projection (%)", "ASTRAL_Score": "Composite Score"},
            title="Regression Vector Distribution Matrix: Patient Variance Mapping",
            color_continuous_scale=px.colors.sequential.Ice_r
        )
        fig_scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='#0F172A',
            font={'color': '#94A3B8', 'family': 'Inter'},
            xaxis={'gridcolor': '#1E293B', 'zerolinecolor': '#1E293B'},
            yaxis={'gridcolor': '#1E293B', 'zerolinecolor': '#1E293B'},
            title_font={'size': 14, 'color': '#F8FAFC', 'family': 'Inter'}
        )
        st.plotly_chart(fig_scatter, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

