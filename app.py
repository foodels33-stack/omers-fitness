import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. הגדרות מיתוג ואייקון כושר (במקום Streamlit) ---
st.set_page_config(
    page_title="Omer's Fitness", 
    layout="centered", 
    page_icon="🏋️"  # זה האייקון שיוצג על שולחן העבודה
)

# עיצוב CSS למראה שחור מקצועי ויוקרתי
style = """
    <style>
    /* רקע שחור עמוק */
    .stApp { background-color: #000000; color: #FFFFFF; }
    
    /* הסתרת רכיבי Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* עיצוב כותרות ומדדים */
    h1, h2, h3 { color: #CCFF00 !important; font-family: 'Arial'; }
    [data-testid="stMetricValue"] { color: #CCFF00; font-weight: bold; }
    
    /* תיבות תוכן מעוצבות */
    .custom-box {
        background-color: #111111; 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid #333333;
        border-right: 5px solid #CCFF00;
        color: #FFFFFF;
        margin-bottom: 20px;
    }
    
    /* כפתור סיום אימון */
    div.stButton > button:first-child {
        background-color: #CCFF00; 
        color: black; 
        font-weight: bold; 
        border-radius: 30px; 
        height: 55px;
        border: none;
        font-size: 1.2rem;
    }
    </style>
"""
st.markdown(style, unsafe_allow_html=True)

# --- 2. מנוע סגמנטציה וחישוב נתונים ---
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

# --- 3. ממשק משתמש וכותרת ---
st.markdown("<h1 style='text-align: center;'>OMER'S FITNESS</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 נתוני לקוח")
    age = st.number_input("גיל", 12, 90, 18)
    height = st.number_input("גובה (ס״מ)", 120, 230, 175)
    weight = st.number_input("משקל (ק״ג)", 30, 200, 65)
    activity = st.select_slider("רמת פעילות", options=[1.2, 1.375, 1.55, 1.725], value=1.55)

plan = analyze_user(weight, height, age, activity)

# תצוגת אבחון
st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("BMI", plan['bmi'])
c2.metric("יעד קלורי", f"{round(plan['cal'])}")
c3.metric("חלבון יומי", f"{round(plan['prot'])}g")

st.markdown(f'<div class="custom-box"><strong>סטטוס:</strong> {plan["status"]} | <strong>אסטרטגיה:</strong> {plan["strat"]}</div>', unsafe_allow_html=True)

# --- 4. תזונה מותאמת ---
st.subheader("🍎 הנחיות תזונה ליום אימון")
with st.expander("צפה בתפריט המומלץ שלך"):
    st.write(f"🍳 **בוקר:** חביתה/ביצים קשות + לחם מלא + אבוקדו.")
    st.write(f"🍗 **צהריים:** חזה עוף או בקר + פחמימה (אורז/בטטה) + ירקות.")
    st.write(f"🍌 **לפני אימון:** בננה או חופן תמרים לאנרגיה זמינה.")
    st.write(f"🥛 **אחרי אימון:** שייק חלבון או טונה + פחמימה להתאוששות.")

st.divider()

# --- 5. יומן אימון וביצוע ---
st.subheader("💪 אימון היום: תיעוד וביצוע")

st.markdown('<div class="custom-box"><strong>📈 התקדמות:</strong> אם סיימת את כל הסטים, באימון הבא תוסיף 2.5 ק"ג לכל צד.</div>', unsafe_allow_html=True)

workout_data = [
    {"name": "סקוואט (Squat)", "sets": 3, "reps": "8-12", "ratio": 0.5},
    {"name": "לחיצת חזה (Bench)", "sets": 3, "reps": "8-12", "ratio": 0.4},
    {"name": "מתח / פולי עליון", "sets": 3, "reps": "10-12", "ratio": 0.35}
]

performed = []

for ex in workout_data:
    suggested = round(weight * ex['ratio'] / 2.5) * 2.5
    with st.expander(f"🏋️ {ex['name']}"):
        st.write(f"יעד: {ex['sets']} סטים X {ex['reps']} חזרות")
        w_lifted = st.number_input(f"משקל (ק״ג)", key=f"w_{ex['name']}", value=float(suggested), step=2.5)
        r_done = st.number_input(f"חזרות בסט אחרון", key=f"r_{ex['name']}", value=10, step=1)
        performed.append({"תרגיל": ex['name'], "משקל (ק״ג)": w_lifted, "חזרות": r_done})

st.divider()

# --- 6. סיכום ויומן סופי ---
if st.button("סכם אימון ושמור ביומן"):
    st.balloons()
    st.header("📋 יומן ביצוע - סיכום האימון")
    
    # הצגת טבלת הביצועים של היום
    summary_df = pd.DataFrame(performed)
    st.table(summary_df)
    
    now = datetime.now().strftime("%d/%m/%Y | %H:%M")
    st.success(f"האימון נחתם בהצלחה בתאריך {now}")
    
    st.markdown(f"""
    <div class="custom-box">
        <strong>מה השגנו היום?</strong><br>
        1. גירוי לצמיחת שריר לפי אסטרטגיית {plan['status']}.<br>
        2. תיעוד מדויק של משקלים לטובת עומס פרוגרסיבי.<br>
        3. עמידה ביעדי האימון של Omer's Fitness.
    </div>
    """, unsafe_allow_html=True)
