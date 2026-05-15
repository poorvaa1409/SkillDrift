import numpy as np
import pickle
import os
import pandas as pd

MODEL = None
SCALER = None

def load_ml_components():
    global MODEL, SCALER
    try:
        model_path = 'models/skill_model.pkl'
        scaler_path = 'models/scaler.pkl'
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            with open(model_path, 'rb') as f:
                MODEL = pickle.load(f)
            with open(scaler_path, 'rb') as f:
                SCALER = pickle.load(f)
            return True
    except Exception as e:
        print(f"Error loading ML components: {e}")
    return False

COMPONENTS_LOADED = load_ml_components()

def predict_drift_status(score):
    if COMPONENTS_LOADED and MODEL and SCALER:
        try:
            input_data = np.array([[score]])
            scaled_input = SCALER.transform(input_data)
            prediction = MODEL.predict(scaled_input)[0]
            
            status_map = {
                0: "High Drift (Critical Revision Needed)",
                1: "Medium Drift (Steady Progress)",
                2: "Low Drift (Advanced Proficiency)"
            }
            return status_map.get(prediction, "Unknown Status")
        except Exception as e:
            print(f"ML Prediction failed: {e}")
            
    if score < 40:
        return "High Drift (Critical Revision Needed)"
    elif score < 75:
        return "Medium Drift (Steady Progress)"
    else:
        return "Low Drift (Advanced Proficiency)"

def get_job_requirements():
    return {
        "SDE": ["DSA", "DBMS", "OS", "System Design", "C++", "Java"],
        "Data Scientist": ["Python", "Statistics", "ML", "DL", "SQL", "Data Visualization"],
        "ML Engineer": ["ML", "DL", "Python", "Mathematics", "Deployment", "DSA"],
        "Frontend Developer": ["HTML", "CSS", "JS", "React", "UI/UX", "Git"],
        "Backend Developer": ["Node.js", "Express", "DBMS", "API Design", "Docker", "Security"]
    }

def analyze_job_match(role, user_scores_df):
    requirements = get_job_requirements().get(role, [])
    if not requirements:
        return None

    user_skills = {}
    if not user_scores_df.empty:
        latest_scores = user_scores_df.sort_values('timestamp').groupby('domain').last()
        for sub, row in latest_scores.iterrows():
            user_skills[sub] = row['score']

    required_skills = requirements
    missing_skills = []
    need_improvement = []
    mastered_skills = []

    for skill in required_skills:
        score = user_skills.get(skill, 0)
        if skill not in user_skills:
            missing_skills.append(skill)
        elif score < 50:
            need_improvement.append(skill)
        else:
            mastered_skills.append(skill)

    return {
        "role": role,
        "required": required_skills,
        "missing": missing_skills,
        "improvement": need_improvement,
        "mastered": mastered_skills
    }
