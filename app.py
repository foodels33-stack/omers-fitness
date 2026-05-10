import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. הגדרות מיתוג ואייקון ---
st.set_page_config(page_title="Omer's Fitness", layout="centered", page_icon="🏋️")

style = """
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    h1, h2, h3 { color: #CCFF00 !important; }
    [data-testid="stMetricValue"] { color: #CCFF00; font-weight: bold; }
    .custom-box {
        background-color: #111111; 
        padding: 20px; border-radius: 12px; border: 1px solid #333333;
        border-right: 5px solid #CCFF00; color: #FFFFFF; margin-bottom: 20px;
    }
    div.stButton > button:first-child {
        background-color: #CCFF00; color: black; font-weight: bold; 
        border-radius: 30px; height: 55px; border: none; font-size: 1.2rem;
    }
    </style>
"""
st.markdown(style, unsafe_allow_html=True)

# --- 2. לוגיקת חישוב ---
def analyze_user(w, h, a, act):
    bmi = w / ((h/100) ** 2)
    bmr = (10 * w) + (6.25 * h) - (5 * a) + 5
    tdee = bmr * act
    if bmi < 18.5:
        res = {"status": "מבנה רזה", "strat": "מסה אגרסיבית", "cal": tdee + 500, "prot": w * 2.2}
    elif 18.5 <= bmi < 25:
        res = {"status": "מבנה אתלטי", "strat": "מסה נקייה", "cal": tdee + 300, "prot": w * 2.0}
    else:
        res = {"status": "מבנה רחב", "strat": "חיטוב ובניית שריר", "cal": tdee - 100, "prot": w * 2.4}
    res["bmi"] = round(bmi, 1)
    return res

# --- 3. ממשק משתמש ---
st.markdown("<h1 style='text-align: center;'>OMER'S FITNESS</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 נתוני לקוח")
    age = st.number_input("גיל", 12, 90, 18)
    height = st.number_input("גובה (ס״מ)", 120, 230, 175)
    weight = st.number_input("משקל (ק״ג)", 30, 200, 65)
    activity = st.select_slider("רמת פעילות", options=[1.2, 1.375, 1.55, 1.725], value=1.55)

plan = analyze_user(weight, height, age, activity)

st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("BMI", plan['bmi'])
c2.metric("יעד קלורי", f"{round(plan['cal'])}")
c3.metric("חלבון יומי", f"{round(plan['prot'])}g")

# --- 4. אימון וביצוע ---
st.subheader("💪 אימון היום")

workout_data = [
    {"name": "סקוואט (Squat)", "sets": 3, "reps": "8-12", "ratio": 0.5},
    {"name": "לחיצת חזה (Bench)", "sets": 3, "reps": "8-12", "ratio": 0.4},
    {"name": "מתח / פולי עליון", "sets": 3, "reps": "10-12", "ratio": 0.35}
]

performed = []
for ex in workout_data:
    suggested = round(weight * ex['ratio'] / 2.5) * 2.5
    with st.expander(f"🏋️ {ex['name']}"):
        w_lifted = st.number_input(f"משקל (ק״ג)", key=f"w_{ex['name']}", value=float(suggested), step=2.5)
        r_done = st.number_input(f"חזרות", key=f"r_{ex['name']}", value=10, step=1)
        performed.append({"תאריך": datetime.now().strftime("%d/%m/%Y"), "תרגיל": ex['name'], "משקל": w_lifted, "חזרות": r_done})

st.divider()

# --- 5. שמירה והצגת יומן ---
if st.button("סכם אימון ושמור"):
    st.balloons()
    df_current = pd.DataFrame(performed)
    
    # הצגת הטבלה על המסך
    st.subheader("📋 סיכום אימון נוכחי")
    st.table(df_current)
    
    # יצירת קובץ להורדה (כך הנתונים נשמרים אצל המשתמש)
    csv = df_current.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 הורד יומן אימונים למכשיר",
        data=csv,
        file_name=f"workout_{datetime.now().strftime('%d_%m_%Y')}.csv",
        mime="text/csv",
    )
    st.success("האימון מוכן להורדה! מומלץ לשמור את הקובץ בתיקייה ייעודית בטלפון.")
