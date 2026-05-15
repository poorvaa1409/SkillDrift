import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import os
import random

from src.database import create_tables, get_user_scores, save_score, get_user_data, update_user_profile
from src.auth import authentication
from src.quiz_engine import get_questions, get_subjects
from src.ml_logic import predict_drift_status, analyze_job_match, get_job_requirements

st.set_page_config(page_title="SkillDrift | AI Skill Intelligence", layout="wide", initial_sidebar_state="expanded")

create_tables()

if os.path.exists("assets/style.css"):
    with open("assets/style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def load_lottie(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

lottie_ai = load_lottie("https://lottie.host/82e2f3d6-4448-4303-9993-f47225102a46/6mH886F6U7.json") 
lottie_book = load_lottie("https://lottie.host/50d3a54d-157d-411a-8e2b-2879685e8a60/uYy3U9U9U9.json") 
lottie_robot = load_lottie("https://lottie.host/86d6303d-d0f7-4a0b-930b-d05542f6f59a/p8N7uI8S1j.json") 

def display_doodle(animation_data, height=150):
    if animation_data:
        st_lottie(animation_data, height=height, key=f"lottie_{random.randint(0, 10000)}")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    selected = option_menu(
        None,
        ["Home", "Login"],
        icons=["house", "person"],
        orientation="horizontal",
        styles={
            "container": {"padding": "5px !important", "background-color": "rgba(15, 23, 42, 0.6)", "border-radius": "15px", "border": "1px solid rgba(34, 211, 238, 0.2)"},
            "icon": {"color": "#22d3ee", "font-size": "20px"},
            "nav-link": {"font-size": "18px", "text-align": "center", "margin":"0px", "--hover-color": "rgba(34, 211, 238, 0.2)", "color": "#e2e8f0"},
            "nav-link-selected": {"background-color": "rgba(34, 211, 238, 0.4)", "color": "#FFFFFF"},
        }
    )

    if selected == "Home":
        st.markdown("""
        <div class='hero'>
            <div class='hero-accent'></div>
            <div class='title-main'>SKILLDRIFT</div>
            <div class='subtitle-main'>
            The Ultimate AI-Powered Skill Gap Analysis Platform. 
            Bridge the gap between your current expertise and industry demands.
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<div class='card-glow'><h3>🤖 Smart AI Analysis</h3><p>Identify drift in your skill set with deep precision.</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='card-glow'><h3>📚 Personalized Paths</h3><p>Custom roadmaps designed for your unique career goals.</p></div>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div class='card-glow'><h3>🎯 Job Alignment</h3><p>Match your skills with top-tier industry roles.</p></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class='about-section'>
            <div class='about-title'>About SkillDrift</div>
            <div class='about-text'>
                SkillDrift empowers developers and students to bridge the gap between where they are and where the industry is going. 
                Our platform uses advanced ML models to analyze your performance and guide your professional evolution.
            </div>
            <div class='credits-box'>
                <span class='credit-item'>Poorva Pancholi</span>
                <span class='credit-item'>Siddharth Toshniwal</span>
                <span class='credit-item'>Soyam Goyal</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif selected == "Login":
        authentication()

else:
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; color: #22d3ee; text-shadow: 0 0 10px rgba(34, 211, 238, 0.5);'>SKILLDRIFT</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #a855f7;'>Session: <b>{st.session_state.username}</b></p>", unsafe_allow_html=True)
        
        menu = option_menu(
            None,
            ["Dashboard", "Quiz", "Job Match", "Profile", "Logout"],
            icons=["bar-chart", "patch-question", "briefcase", "person-badge", "box-arrow-right"],
            default_index=0,
            styles={
                "container": {"padding": "5px !important", "background-color": "transparent"},
                "icon": {"color": "#22d3ee", "font-size": "18px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"5px", "--hover-color": "rgba(34, 211, 238, 0.1)", "color": "#e2e8f0"},
                "nav-link-selected": {"background-color": "rgba(34, 211, 238, 0.3)", "border-left": "4px solid #22d3ee"},
            }
        )
        
        if st.button("⬅ Home", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    if menu == "Dashboard":
        st.markdown("<h1 class='title-main'>Dashboard</h1>", unsafe_allow_html=True)
        df = get_user_scores(st.session_state.username)
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"<div class='card-glow'><h3>Latest Score</h3><h1 style='color: #22d3ee;'>{int(df['score'].iloc[-1])}%</h1></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='card-glow'><h3>Average</h3><h1 style='color: #a855f7;'>{int(df['score'].mean())}%</h1></div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='card-glow'><h3>Total Assessments</h3><h1 style='color: #22d3ee;'>{len(df)}</h1></div>", unsafe_allow_html=True)

            st.markdown("<div class='card-glow'><h3>Performance Trend</h3>", unsafe_allow_html=True)
            fig = px.line(df, x="timestamp", y="score", markers=True, line_shape="spline", template="plotly_dark")
            fig.update_traces(line=dict(width=5, color='#22d3ee'), marker=dict(size=14, symbol="diamond", line=dict(width=2, color="white"), color='#a855f7'))
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", 
                paper_bgcolor="rgba(0,0,0,0)", 
                font=dict(color="#e2e8f0"), 
                xaxis=dict(showgrid=False), 
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)")
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            with st.expander("Detailed Assessment History"):
                st.dataframe(df.sort_values('timestamp', ascending=False), use_container_width=True)
        else:
            st.info("Your dashboard is empty. Take a quiz to begin!")
            display_doodle(lottie_robot)

    elif menu == "Quiz":
        st.markdown("<h1 class='title-main'>AI Challenge</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        with col1:
            domain = st.selectbox("Select Domain", ["Programming Languages", "Web Development", "CSE Core", "Data Science & AI"])
            subject = st.selectbox("Select Subject", get_subjects(domain))
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Generate 10 Questions"):
                with st.spinner("Crafting your AI challenge..."):
                    st.session_state.questions = get_questions(subject, count=10)
                    st.session_state.start = True

        if st.session_state.get("start"):
            answers = {}
            for i, q in enumerate(st.session_state.questions):
                st.markdown(f"<div class='card-glow'><h4>Q{i+1}. {q['q']}</h4></div>", unsafe_allow_html=True)
                answers[i] = st.radio("Option", q["o"], index=None, key=f"q_{i}", label_visibility="collapsed")

            if st.button("Submit Assessment"):
                score = 0
                results = []
                for i, q in enumerate(st.session_state.questions):
                    correct = (answers[i] == q["a"])
                    if correct: score += 1
                    results.append({"q": q["q"], "user": answers[i], "correct": q["a"], "is_correct": correct})

                perc = (score / len(st.session_state.questions)) * 100
                status = predict_drift_status(perc)
                
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.markdown(f"<div class='card-pastel card-pastel-blue'><h2>Result: {perc:.1f}%</h2><p>{status}</p></div>", unsafe_allow_html=True)
                
                with st.expander("Review Your Performance"):
                    for r in results:
                        color = "green" if r['is_correct'] else "red"
                        st.markdown(f"**Q:** {r['q']}\n\n**Your Ans:** :{color}[{r['user']}] | **Correct:** :green[{r['correct']}]")
                
                save_score(st.session_state.username, subject, perc, status)
                st.balloons()
                st.session_state.start = False

    elif menu == "Job Match":
        st.markdown("<h1 class='title-main'>Job Matching</h1>", unsafe_allow_html=True)
        df = get_user_scores(st.session_state.username)
        roles = list(get_job_requirements().keys())
        role = st.selectbox("Select Target Role", roles)
        analysis = analyze_job_match(role, df)
        
        if analysis:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("<div class='card-glow'><h3>Role Requirements</h3>", unsafe_allow_html=True)
                for s in analysis['required']: st.write(f"• {s}")
                st.markdown("</div>", unsafe_allow_html=True)
            with c2:
                if analysis['missing']:
                    st.markdown("<div class='card-pastel card-pastel-red'><h4>🚨 Skill Drift Detected</h4>", unsafe_allow_html=True)
                    for s in analysis['missing']: st.write(f"• {s}")
                    st.markdown("</div>", unsafe_allow_html=True)
                if analysis['mastered']:
                    st.markdown("<div class='card-pastel card-pastel-green'><h4>✅ Current Proficiencies</h4>", unsafe_allow_html=True)
                    for s in analysis['mastered']: st.write(f"• {s}")
                    st.markdown("</div>", unsafe_allow_html=True)

    elif menu == "Profile":
        st.markdown("<h1 class='title-main'>Intelligence Profile</h1>", unsafe_allow_html=True)
        user = get_user_data(st.session_state.username)
        
        if user and len(user) >= 7:
            name_val, cid_val, year_val, bio_val = user[3], user[4], user[5], user[6]
        else:
            name_val, cid_val, year_val, bio_val = "", "", "1st", ""

        with st.form("ProfileForm"):
            name = st.text_input("Full Name", name_val if name_val else "")
            cid = st.text_input("College/Institution ID", cid_val if cid_val else "")
            year = st.selectbox("Current Year", ["1st", "2nd", "3rd", "4th"], index=["1st", "2nd", "3rd", "4th"].index(year_val if year_val else "1st"))
            bio = st.text_area("Professional Bio", bio_val if bio_val else "")
            if st.form_submit_button("Save Changes"):
                update_user_profile(st.session_state.username, name, cid, year, bio)
                st.success("Profile intelligence updated!")

    elif menu == "Logout":
        st.session_state.logged_in = False
        st.rerun()
