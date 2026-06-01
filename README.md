# Acute Ischemic Stroke Decision Support Architecture
### Advanced Predictive Modeling & Clinical Analytics for 3-Month Functional Outcomes

##  Clinical Overview
This repository hosts a production-grade, open-source clinical informatics dashboard implementing the peer-reviewed **ASTRAL (Acute Stroke Registry and Analysis of Lausanne) Protocol**. The system quantifies the mathematical probability of an unfavorable 3-month functional outcome (Modified Rankin Scale score of 3–6) following acute ischemic events.

*   **Live Application URL:** https://elite-stroke-analytics-jdb8ne7th3vtrmqmvhwgzz.streamlit.app/
*   **Source Code Matrix:** https://github.com/noorfatimacheema249-design/elite-stroke-analytics

##  Technical Stack & Architecture
- **Language Framework:** Python 3.11+
- **User Interface Layer:** Streamlit Architecture (Reactive design system)
- **Data Visualization Engine:** Plotly Express (Interactive multidimensional matrices)
- **Document Compiling Layer:** ReportLab Canvas Engine (Automated clinical PDF rendering)
- **Statistical Operations:** NumPy & Pandas Engine

##  Core Features & Implementation Models
1. **Intake Metrics Pipeline:** Processes baseline patient parameters including age indexes, metabolic serum profiles, door-to-needle time delay flags, and National Institutes of Health Stroke Scale (NIHSS) neurological deficits.
2. **Monte Carlo Bootstrapping Simulator:** Runs a 500-iteration statistical simulation to output valid 95% confidence intervals, modeling systemic clinical uncertainty.
3. **Automated Documentation Engine:** Instantly compiles user metrics into a secure, publication-grade PDF clinical brief for institutional quality tracking.
4. **Registry Simulation Studio:** Generates custom synthetic patient evaluation cohorts (N=500) to trace multi-variable risk distributions and regression matrices.

##  Scientific Validation Data
The integer scoring point allocation logic exactly replicates the criteria published by Ntaios et al. in *Neurology* (2012). Downstream probability estimations utilize optimized logistic regression curves derived from standard baseline validation data profiles.

*Disclaimer: This repository represents an educational proof-of-concept for institutional portfolio review and clinical informatics simulation. It is strictly isolated from live patient management channels.*
Use code with caution.Step 3: Push Document Updates LiveOpen your Git PowerShell console window and run this sequence to sync these additions instantly to your public profile view:powershellgit add LICENSE README.md
git commit -m "Documentation: Finalized MIT License deployment and academic README layout matrices"
git push origin main
