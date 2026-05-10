import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. הגדרות דף ועיצוב (Inspired by Pro Fitness Apps) ---
st.set_page_config(
    page_title="Omer's Fitness 2.0",
    page_icon="🏋️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. מנוע עיצוב מותאם אישית (Custom CSS) ---
# עיצוב בסגנון Dark Mode מקצועי עם צבעי אקסנט ירוק-ליים
st.markdown("""
    <style>
        /* הגדרות רקע וצבעים כלליות */
        .stApp {
            background-color: #000000;
            color: #E0E0E0;
            max-width: 100%;
            padding: 1rem !important; /* תוספת לסלולר */
        }
        
        /* כותרות בסגנון כושר */
        h1, h2, h3 {
            color: #ccff00 !important; /* Lime Green - אנרגטי ומודרני */
            font-family: 'Inter', sans-serif;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            text-align: center;
        }

        /* עיצוב כרטיסיות מידע (Info Cards) */
        .fitness-card {
            background-color: #1a1a1a;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(204, 255, 0, 0.1);
        }
        
        /* עיצוב המטריקות (מאקרו) */
        .stMetricValue {
            color: #ccff00 !important;
            font-size: 32px !important;
        }
        .stMetricLabel {
            color: #A0A0A0 !important;
        }

        /* עיצוב כפתורים */
        div.stButton > button:first-child {
            background-color: #ccff00;
            color: #000;
            border-radius: 30px;
            font-weight: bold;
            width: 100%;
            border: none;
            text-transform: uppercase;
        }
        
        div.stButton > button:first-child:hover {
            background-color: #4ade80;
            color: #000;
        }

        /* עיצוב סרגל צד (Sidebar) - Dark Mode */
        .stSidebar {
            background-color: #0a0a0a;
        }

    </style>
    """, unsafe_allow_html=True)

# --- 3. מאגר נתונים ולוגיקה (בסיס מדעי) ---
EXERCISES_DB = {
    "סקוואט (Squats)": {"target": "רגליים", "tip": "שמור על גב ישר, רד עם הישבן נמוך."},
    "לחיצת חזה (Bench Press)": {"target": "חזה, כתפיים", "tip": "הצמד את השכמות לספסל."},
    "מתח / פולי עליון": {"target": "גב, יד קדמית", "tip": "תחשוב על למשוך עם המרפקים."},
    "לחיצת כתפיים (Shoulder Press)": {"target": "כתפיים, יד אחורית", "tip": "אל תקשת את הגב התחתון."}
}

def calculate_macros(w, h, a, act):
    bmr = (10 * w) + (6.25 * h) - (5 * a) + 5
    tdee = bmr * act
    target_cal = tdee + 350 # עודף קלורי מבוקר למסה
    # חלוקת מאקרו מבוססת עקרונות ISSN
    protein = w * 2.0
    fats = (target_cal * 0.25) / 9
    carbs = (target_cal - (protein * 4) - (fats * 9)) / 4
    return round(target_cal), round(protein), round(fats), round(carbs)

# --- 4. הממשק המרכזי ---
st.title("🏋️ Omer's Fitness")

# סרגל צד - נתונים אישיים ומוזיקה
with st.sidebar:
    st.header("👤 פרופיל")
    age = st.number_input("גיל", value=16)
    weight = st.number_input("משקל (קג)", value=60.0)
    height = st.number_input("גובה (סמ)", value=175)
    activity = st.select_slider("רמת פעילות", options=[1.2, 1.375, 1.55, 1.725], value=1.55)
    
    st.divider()
    st.subheader("🎵 Workout Playlist")
    playlist_url = "https://open.spotify.com/embed/playlist/37i9dQZF1DX70UOzfvYubW" 
    st.markdown(f"""
        <iframe src="{playlist_url}" width="100%" height="80" 
        frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
    """, unsafe_allow_html=True)

# כרטיסיית יעדים בראש המסך
cal, prot, fat, carb = calculate_macros(weight, height, age, activity)
with st.container():
    st.markdown('<div class="fitness-card">', unsafe_allow_html=True)
    st.subheader("🎯 יעד יומי למסה")
    cols = st.columns(4)
    cols[0].metric("קלוריות", f"{cal}")
    cols[1].metric("חלבון", f"{prot}g")
    cols[2].metric("פחמימה", f"{carb}g")
    cols[3].metric("שומן", f"{fat}g")
    st.markdown('</div>', unsafe_allow_html=True)

# תוכנית האימונים - כרטיסיות נפרדות לכל תרגיל
st.subheader("💪 לוג אימון יומי (Full Body)")
for ex, info in EXERCISES_DB.items():
    with st.container():
        st.markdown(f'<div class="fitness-card">', unsafe_allow_html=True)
        col_title, col_status = st.columns([2, 1])
        col_title.markdown(f"**{ex}** - <span style='color:#A0A0A0'>{info['target']}</span>", unsafe_allow_html=True)
        col_status.write("") # מקום לסטטוס עתידי (DONE)
        
        # טיפ מקצועי
        st.info(f"💡 {info['tip']}")
        
        c1, c2 = st.columns(2)
        w_input = c1.number_input("משקל (קג)", key=f"w_{ex}", step=0.5)
        r_input = c2.number_input("חזרות", key=f"r_{ex}", step=1)
        
        if st.button(f"שמור סט ל-{ex}", key=f"b_{ex}"):
            st.success(f"נשמר: {w_input} ק\"ג X {r_input} חזרות. קדימה!")
        st.markdown('</div>', unsafe_allow_html=True)

# כרטיסיית תזונה קבועה
st.divider()
with st.container():
    st.markdown('<div class="fitness-card">', unsafe_allow_html=True)
    st.subheader("🍴 תפריט תזונה מומלץ")
    st.write(f"""
    * **ארוחת בוקר:** שייק מסה (כוס חלב, 1 בננה, 3 כפות שיבולת שועל, כף חמאת בוטנים).
    * **צהריים:** 200 גרם חזה עוף/בקר, 2 כוסות אורז מלא, אבוקדו.
    * **אחרי אימון:** יוגורט חלבון + פרי (תפוח/תמר).
    * **ערב:** חביתה מ-2 ביצים, קוטג', ירקות ירוקים, פרוסת לחם מלא.
    """)
    st.markdown('</div>', unsafe_allow_html=True)