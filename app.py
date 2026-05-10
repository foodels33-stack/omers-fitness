import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. הגדרות דף ועיצוב ---
st.set_page_config(
    page_title="Omer's Fitness 2.0",
    page_icon="🏋️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. מנוע עיצוב מותאם אישית ---
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stAppDeployButton {display:none;}
        
        .stApp {
            background-color: #000000;
            color: #E0E0E0;
            max-width: 100%;
            padding: 1rem !important;
        }
        
        h1, h2, h3 {
            color: #ccff00 !important;
            font-family: 'Inter', sans-serif;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            text-align: center;
        }

        .fitness-card {
            background-color: #1a1a1a;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(204, 255, 0, 0.1);
        }
        
        .stMetricValue {
            color: #ccff00 !important;
            font-size: 32px !important;
        }

        div.stButton > button:first-child {
            background-color: #ccff00;
            color: #000;
            border-radius: 30px;
            font-weight: bold;
            width: 100%;
            border: none;
            text-transform: uppercase;
            height: 3em;
        }

        .block-container {
            padding-top: 1rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

# --- 3. לוגיקה ---
def calculate_macros(w, h, a, act):
    bmr = (10 * w) + (6.25 * h) - (5 * a) + 5
    tdee = bmr * act
    target_cal = tdee + 350
    protein = w * 2.0
    fats = (target_cal * 0.25) / 9
    carbs = (target_cal - (protein * 4) - (fats * 9)) / 4
    return round(target_cal), round(protein), round(fats), round(carbs)

EXERCISES_DB = {
    "סקוואט (Squats)": {"target": "רגליים", "tip": "גב ישר, לרדת נמוך."},
    "לחיצת חזה (Bench)": {"target": "חזה", "tip": "שכמות צמודות לספסל."},
    "מתח / פולי עליון": {"target": "גב", "tip": "למשוך עם המרפקים."},
    "לחיצת כתפיים": {"target": "כתפיים", "tip": "בטן חזקה, לא לקשת גב."}
}

# --- 4. הממשק המרכזי ---
st.title("🏋️ Omer's Fitness")

# סרגל צד לנתונים אישיים בלבד
with st.sidebar:
    st.header("👤 פרופיל")
    age = st.number_input("גיל", value=16)
    weight = st.number_input("משקל (קג)", value=60.0)
    height = st.number_input("גובה (סמ)", value=175)
    activity = st.select_slider("רמת פעילות", options=[1.2, 1.375, 1.55, 1.725], value=1.55)

# כרטיסיית יעדים
cal, prot, fat, carb = calculate_macros(weight, height, age, activity)
st.markdown('<div class="fitness-card">', unsafe_allow_html=True)
st.subheader("🎯 יעד יומי למסה")
c1, c2, c3, c4 = st.columns(4)
c1.metric("קלוריות", cal)
c2.metric("חלבון", f"{prot}g")
c3.metric("פחמימה", f"{carb}g")
c4.metric("שומן", f"{fat}g")
st.markdown('</div>', unsafe_allow_html=True)

# --- מוזיקה במסך הראשי ---
st.markdown('<div class="fitness-card">', unsafe_allow_html=True)
st.subheader("🎵 מוזיקה לאימון")
playlist_url = "https://open.spotify.com/embed/playlist/37i9dQZF1DX76W9SwwE6v4" # פלייליסט מוטיבציה
st.markdown(f'<iframe src="{playlist_url}" width="100%" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# תוכנית אימון
st.subheader("💪 לוג אימון")
for ex, info in EXERCISES_DB.items():
    with st.container():
        st.markdown('<div class="fitness-card">', unsafe_allow_html=True)
        st.markdown(f"**{ex}** | <span style='color:#A0A0A0'>{info['target']}</span>", unsafe_allow_html=True)
        st.info(f"💡 {info['tip']}")
        col1, col2 = st.columns(2)
        w_in = col1.number_input("קילוגרם", key=f"w_{ex}", step=0.5)
        r_in = col2.number_input("חזרות", key=f"r_{ex}", step=1)
        if st.button(f"סיום סט", key=f"b_{ex}"):
            st.success(f"נשמר!")
        st.markdown('</div>', unsafe_allow_html=True)

# תפריט תזונה
st.divider()
st.markdown('<div class="fitness-card">', unsafe_allow_html=True)
st.subheader("🍴 תפריט יומי מומלץ")
st.write("""
* **בוקר:** שייק מסה (חלב, בננה, שיבולת שועל, חמאת בוטנים).
* **צהריים:** 200ג חלבון (עוף/בקר) + 2 כוסות אורז מבושל + ירקות.
* **אחה"צ:** יוגורט חלבון או פרי.
* **ערב:** חביתה מ-2 ביצים, גבינה, אבוקדו, לחם מלא.
""")
st.markdown('</div>', unsafe_allow_html=True)
