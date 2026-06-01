import numpy as np

def calculate_astral_probability(age: int, nihss: int, time_delay_hours: float, 
                                 visual_defect: bool, glucose_mmol: float, 
                                 impaired_loc: bool) -> dict:
    age_points = age // 5
    nihss_points = nihss
    time_points = 2 if time_delay_hours > 3.0 else 0
    visual_points = 2 if visual_defect else 0
    glucose_points = 1 if (glucose_mmol > 7.3 or glucose_mmol < 3.7) else 0
    loc_points = 3 if impaired_loc else 0
    
    total_score = age_points + nihss_points + time_points + visual_points + glucose_points + loc_points

    logit_intercept = -4.95 
    logit_coefficient = 0.245 
    
    patient_logit = logit_intercept + (logit_coefficient * total_score)
    probability = 1 / (1 + np.exp(-patient_logit))
    
    np.random.seed(42)
    simulated_logits = patient_logit + np.random.normal(0, 0.25, 500)
    simulated_probs = 1 / (1 + np.exp(-simulated_logits))
    ci_lower = np.percentile(simulated_probs, 2.5)
    ci_upper = np.percentile(simulated_probs, 97.5)

    return {
        "score": total_score,
        "probability": float(probability),
        "ci_lower": float(ci_lower),
        "ci_upper": float(ci_upper),
        "breakdown": {
            "Age Index": age_points,
            "Neurological Deficit (NIHSS)": nihss_points,
            "Thrombolysis Delay Factor": time_points,
            "Visual Pathway Defect": visual_points,
            "Metabolic Disruption (Glucose)": glucose_points,
            "Consciousness Depression": loc_points
        }
    }

def generate_synthetic_cohort(size: int = 100):
    np.random.seed(101)
    ages = np.random.randint(40, 90, size)
    nihss = np.random.randint(2, 28, size)
    delays = np.random.uniform(0.5, 8.0, size)
    visual = np.random.choice([True, False], size, p=[0.3, 0.7])
    glucose = np.random.uniform(3.0, 15.0, size)
    loc = np.random.choice([True, False], size, p=[0.2, 0.8])
    
    records = []
    for i in range(size):
        res = calculate_astral_probability(ages[i], nihss[i], delays[i], visual[i], glucose[i], loc[i])
        records.append({
            "Patient_ID": f"ST-2026-{i+1000}",
            "Age": int(ages[i]),
            "Baseline_NIHSS": int(nihss[i]),
            "Onset_To_Door_Hrs": round(float(delays[i]), 1),
            "ASTRAL_Score": int(res["score"]),
            "Unfavorable_Outcome_Risk": round(float(res["probability"] * 100), 1)
        })
    return records

