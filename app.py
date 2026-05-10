import streamlit as st

# --- 1. הגדרות דף ועיצוב ---
st.set_page_config(
    page_title="Omer's Fitness",
    page_icon="🏋️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS להסתרת ממשק ועיצוב המותג ---
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stAppDeployButton {display:none;}
        
        .stApp {
            background-color: #000000;
            color: #E0E0E0;
        }
        
        h1, h2, h3 {
            color: #ccff00 !important;
            text-align: center;
        }

        .fitness-card {
            background-color: #1a1a1a;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(204, 255, 0, 0.1);
        }
        
        .stMetricValue {
            color: #ccff00 !important;
            font-size: 28px !important;
        }

        div.stButton > button:first-child {
            background-color: #ccff00;
            color: #000;
            border-radius: 30px;
            font-weight: bold;
            width: 100%;
            border: none;
            height: 3em;
        }
        
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 5rem !important;
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
    "סקוואט (Squats)": {"target": "רגליים", "tip": "גב ישר, רד נמוך עם הישבן."},
    "לחיצת חזה (Bench Press)": {"target": "חזה", "tip": "הצמד שכמות לספסל."},
    "מתח / פולי עליון": {"target": "גב", "tip": "תמשוך מהמרפקים."},
    "לחיצת כתפיים": {"target": "כתפיים", "tip": "בטן חזקה, אל תקשת גב."}
}

# --- 4. הממשק המרכזי ---
st.title("🏋️ Omer's Fitness")

with st.sidebar:
    st.header("👤 נתונים אישיים")
    age = st.number_input("גיל", value=16)
    weight = st.number_input("משקל (קג)", value=60.0)
    height = st.number_input("גובה (סמ)", value=175)
    activity = st.select_slider("רמת פעילות", options=[1.2, 1.375, 1.55, 1.725], value=1.55)

# יעדי תזונה
cal, prot, fat, carb = calculate_macros(weight, height, age, activity)
st.markdown('<div class="fitness-card">', unsafe_allow_html=True)
st.subheader("🎯 יעד יומי למסה")
c1, c2, c3, c4 = st.columns(4)
c1.metric("קלוריות", cal)
c2.metric("חלבון", f"{prot}g")
c3.metric("פחמימה", f"{carb}g")
c4.metric("שומן", f"{fat}g")
st.markdown('</div>', unsafe_allow_html=True)

# --- מוזיקה ---
st.markdown('<div class="fitness-card">', unsafe_allow_html=True)
st.subheader("🎵 פסקול האימון")

music_option = st.radio(
    "בחר אווירה:",
    ["מוזיקה מקורית", "רוק", "אלקטרוני"],
    horizontal=True
)

if music_option == "מוזיקה מקורית":
    try:
        audio_file = open('workout_track.mp3', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3', loop=True)
    except FileNotFoundError:
        st.info("כדי לשמוע את המוזיקה המקורית, העלה קובץ בשם workout_track.mp3 ל-GitHub.")

elif music_option == "רוק":
    st.markdown("""<iframe width="100%" height="180" src="https://www.youtube.com/embed/5S6p_7q7kEw" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>""", unsafe_allow_html=True)

else:
    st.markdown("""<iframe width="100%" height="180" src="https://www.youtube.com/embed/4pD_v_7E60s" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# לוג אימון
st.subheader("💪 לוג אימון")
for ex, info in EXERCISES_DB.items():
    st.markdown('<div class="fitness-card">', unsafe_allow_html=True)
    st.markdown(f"**{ex}** | {info['target']}")
    st.info(f"💡 {info['tip']}")
    col1, col2 = st.columns(2)
    col1.number_input("קג", key=f"w_{ex}", step=0.5)
    col2.number_input("חזרות", key=f"r_{ex}", step=1)
    if st.button(f"שמור סט", key=f"b_{ex}"):
        st.success(f"נשמר!")
    st.markdown('</div>', unsafe_allow_html=True)

# תפריט
st.divider()
st.markdown('<div class="fitness-card">', unsafe_allow_html=True)
st.subheader("🍴 תפריט יומי לדוגמה")
st.write("* **צהריים:** 200ג חלבון + 2 כוסות אורז מבושל.")
st.markdown('</div>', unsafe_allow_html=True)
