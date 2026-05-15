# SkillDrift 🎯
### A Web Based Skill Drift Detection System

SkillDrift is an AI-powered web application that helps students 
and professionals detect their skill drift and get personalized 
job-role matching guidance.

## Features
- Quiz-based skill assessment (12 subjects, 4 domains)
- ML-based drift classification (Low / Medium / High)
- Job match analysis for 5 software engineering roles
- Performance dashboard with score history

## Tech Stack
Python | Streamlit | SQLite | scikit-learn | Google Gemini API

## 🤖 ML & Data Science Components

| Component | Technology | Details |
|---|---|---|
| Drift Classifier | Random Forest (scikit-learn) | 3-class classification — Low / Medium / High Drift |
| Feature Scaling | StandardScaler | Normalizes quiz score (0–100) before ML inference |
| Model Storage | Python Pickle | skill_model.pkl + scaler.pkl — loaded at startup |
| Question Generation | Google Gemini API (LLM) | Dynamic MCQ generation using prompt engineering |
| Data Analysis | Pandas + NumPy | Score aggregation, trend analysis, job match logic |
| Visualization | Plotly Express | Interactive score history chart on dashboard |
| Database | SQLite | Stores user profiles and all quiz performance data |

## Team
- Poorva Pancholi
- Siddharth Toshniwal  

IPS Academy, CSE (Data Science) | 2025-26

## How to Run
1. pip install -r requirements.txt
2. streamlit run app.py
