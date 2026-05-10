import streamlit as st
import pandas as pd

# --- 1. הגדרות דף ועיצוב (Branding) ---
st.set_page_config(
    page_title="Omer's Fitness",
    page_icon="🏋️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS מתקדם להסתרת ממשק הניהול ועיצוב המותג ---
st.markdown("""
    <style>
        /* הסתרת אלמנטים של המערכת (שלא יראו את ממשק הניהול) */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stAppDeployButton {display:none;}
        
        /* עיצוב כללי - Dark Mode */
        .stApp {
            background-color: #000000;
            color: #E0E0E0;
        }
        
        /* כותרות בצבע ליים-גרין */
        h1, h2, h3 {
            color: #ccff00 !important;
            font-family: 'Inter', sans-serif;
            text-transform: uppercase;
            text-align: center;
        }

        /* כרטיסיות מידע (Cards) */
        .fitness-card {
            background-color: #1a1a1a;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(204, 255, 0, 0.1);
        }
        
        /* עיצוב המטריקות */
        .stMetricValue {
            color: #ccff00 !important;
            font-size: 28px !important;
        }

        /* כפתורים מעוגלים ובולטים */
        div.stButton > button:first-child {
            background-color: #ccff00;
            color: #000;
            border-radius: 30px;
            font-weight: bold;
            width: 100%;
            border: none;
            height: 3em;
        }
        
        /* התאמה לסלולר */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 5rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

# --- 3. לוגיקה וחישובים ---
def calculate_macros(w, h, a, act):
    bmr = (10 * w) + (6.25 * h) - (5 * a) + 5
    tdee = bmr * act
    target_cal = tdee + 350 # עודף קלורי למסה
    protein = w * 2.0
    fats = (target_cal * 0.25) / 9
    carbs = (target_cal - (protein * 4) - (fats * 9)) / 4
    return round(target_cal), round(protein), round(fats), round(carbs)

EXERCISES_DB = {
    "סקוואט (Squats)": {"target": "רגליים", "tip": "גב ישר, רד נמוך עם הישבן."},
    "לחיצת חזה (Bench Press)": {"target": "חזה", "tip": "הצמד שכמות לספסל."},
    "מתח / פולי עליון": {"target": "גב", "tip": "תמשוך מהמרפקים."},
    "לחיצת כתפיים": {"target": "כתפיים", "tip": "בטן חזקה, אל תקשת גב."}
}

# --- 4. הממשק המרכזי ---
st.title("🏋️ Omer's Fitness")

# סרגל צד לנתונים אישיים
with st.sidebar:
    st.header("👤 נתונים אישיים")
    age = st.number_input("גיל", value=16)
    weight = st.number_input("משקל (קג)", value=60.0)
    height = st.number_input("גובה (סמ)", value=175)
    activity = st.select_slider("רמת פעילות", options=[1.2, 1.375, 1.55, 1.725], value=1.55)

# --- כרטיסיית יעדי תזונה ---
cal, prot, fat, carb = calculate_macros(weight, height, age, activity)
st.markdown('<div class="fitness-card">', unsafe_allow_html=True)
st.subheader("🎯 יעד יומי למסה")
c1, c2, c3, c4 = st.columns(4)
c1.metric("קלוריות", cal)
c2.metric("חלבון", f"{prot}g")
c3.metric("פחמימה", f"{carb}g")
c4.metric("שומן", f"{fat}g")
st.markdown('</div>', unsafe_allow_html=True)

# --- תפריט מוזיקה מתקדם ---
st.markdown('<div class="fitness-card">', unsafe_allow_html=True)
st.subheader("🎵 פסקול האימון")

music_option = st.radio(
    "בחר אווירה:",
    ["מוזיקה מקורית (Loop)", "רוק (YouTube)", "אלקטרוני (YouTube)"],
    horizontal=True
)

if music_option == "מוזיקה מקורית (Loop)":
    try:
        audio_file = open('workout_track.mp3', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3', loop=True)
        st.caption("מנגן את רצועת הבית של האפליקציה בלולאה")
    except FileNotFoundError:
        st.info("כדי לשמוע את המוזיקה המקורית, העלה קובץ בשם workout_track.mp3 ל-GitHub.")

elif music_option == "רוק (YouTube)":
    st.markdown("""
        <iframe width="100%" height="180" src="https://www.youtube.com/embed/videoseries?list=PLzCxunOM5WFLNCSF0UEHZqFJJ6EceL7Fv" 
        frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
        <iframe width="100%" height="180" src="https://www.youtube.com/embed/videoseries?list=PL467F6D43B604771C" 
        frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- לוג אימון ---
st.subheader("💪 לוג אימון")
for ex, info in EXERCISES_DB.items():
    with st.container():
        st.markdown('<div class="fitness-card">', unsafe_allow_html=True)
        st.markdown(f"**{ex}** | <span style='color:#A0A0A0'>{info['target']}</span>", unsafe_allow_html=True)
        st.info(f"💡 {info['tip']}")
        col1, col2 = st.columns(2)
        w_in = col1.number_input("קג", key=f"w_{ex}", step=0.5)
        r_in = col2.number_input("חזרות", key=f"r_{ex}", step=1)
        if st.button(f"שמור סט", key=f"b_{ex}"):
            st.success(f"הסט נשמר!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- תפריט תזונה מומלץ ---
st.divider()
st.markdown('<div class="fitness-card">', unsafe_allow_html=True)
st.subheader("🍴 תפריט יומי לדוגמה")
st.write(f"""
* **בוקר:** שייק מסה עשיר (חלב, שיבולת שועל, חמאת בוטנים).
* **צהריים:** 200ג חלבון + **2 כוסות אורז מבושל** + ירקות ירוקים.
* **אחה"צ:** יוגורט חלבון + פרי או חטיף אנרגיה.
* **ערב:** חביתה מ-2 ביצים, חצי אבוקדו, גבינה ו-3 פרוסות לחם מלא.
""")
st.markdown('</div>', unsafe_allow_html=True)
