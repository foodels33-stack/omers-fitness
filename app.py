import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. הגדרות מיתוג ואייקון כושר (יפיע בטאב ובשולחן עבודה) ---
st.set_page_config(
    page_title="Omer's Fitness", 
    layout="centered", 
    page_icon="🏋️"
)

# עיצוב CSS למראה שחור יוקרתי (Dark Mode) ללא לוגו Streamlit
style = """
    <style>
    /* רקע שחור עמוק לכל האפליקציה */
    .stApp { background-color: #000000; color: #FFFFFF; }
    
    /* הסתרת רכיבי מערכת של Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* עיצוב כותרות ומדדים בצבע ניאון */
    h1, h2, h3 { color: #CCFF00 !important; font-family: 'Arial', sans-serif; }
    [data-testid="stMetricValue"] { color: #CCFF00 !important; font-weight: bold; }
    
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
    
    /* עיצוב כפתורים */
    div.stButton > button:first-child {
        background-color: #CCFF00; 
        color: black; 
        font-weight: bold; 
        border-radius: 30px; 
        height: 55px;
        border: none;
        font-size: 1.2rem;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #aacc00;
        transform: scale(1.02);
    }
    
    /* עיצוב אקורדיון (תרגילים) */
    .stExpander { border: 1px solid #333333; border-radius: 10px; background-color: #0a0a0a; }
    </style>
"""
st.markdown(style, unsafe_allow_html=True)

# --- 2. מנוע סגמנטציה וחישוב AI ---
def analyze_user(w, h, a, act):
    bmi = w / ((h/100) ** 2)
    bmr = (10 * w) + (6.25 * h) - (5 * a) + 5
    tdee = bmr * act
    
    if bmi < 18.5:
        res = {"status": "מבנה רזה (Ectomorph)", "strat": "מסה אגרסיבית", "cal": tdee + 500, "prot": w * 2.2, "focus": "תרגילים מורכבים, משקלים כבדים ומנוחות ארוכות."}
    elif 18.5 <= bmi < 25:
        res = {"status": "מבנה אתלטי (Mesomorph)", "strat": "מסה נקייה", "cal": tdee + 300, "prot": w * 2.0, "focus": "שילוב של כוח ונפח אימון (Hypertrophy)."}
    else:
        res = {"status": "מבנה רחב (Endomorph)", "strat": "חיטוב ובניית שריר", "cal": tdee - 100, "prot": w * 2.4, "focus": "נפח גבוה, מנוחות קצרות ודופק גבוה."}
    
    res["bmi"] = round(bmi, 1)
    return res

# --- 3. ממשק משתמש וכותרת ---
st.markdown("<h1 style='text-align: center;'>OMER'S FITNESS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Smart Personal Training System</p>", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 נתוני לקוח")
    age = st.number_input("גיל", 12, 90, 18)
    height = st.number_input("גובה (ס״מ)", 120, 230, 175)
    weight = st.number_input("משקל (ק״ג)", 30, 200, 65)
    activity = st.select_slider("רמת פעילות", options=[1.2, 1.375, 1.55, 1.725], value=1.55,
                               format_func=lambda x: "נמוכה" if x==1.2 else "בינונית" if x==1.55 else "גבוהה")

plan = analyze_user(weight, height, age, activity)

# תצוגת אבחון
st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("BMI", plan['bmi'])
c2.metric("יעד קלורי", f"{round(plan['cal'])}")
c3.metric("חלבון יומי", f"{round(plan['prot'])}g")

st.markdown(f'<div class="custom-box"><strong>סטטוס גופני:</strong> {plan["status"]}<br><strong>אסטרטגיה:</strong> {plan["strat"]}<br><strong>דגש אימון:</strong> {plan["focus"]}</div>', unsafe_allow_html=True)

# --- 4. תוכנית תזונה יומית ---
st.subheader("🍎 תפריט תזונה מותאם ליום אימון")
with st.expander("לחץ לצפייה בתפריט היומי"):
    st.write(f"🍳 **בוקר:** חביתה מ-3 ביצים או שייק חלבון עם שיבולת שועל + חמאת בוטנים.")
    st.write(f"🍗 **צהריים:** 200ג חזה עוף/בקר/דג + 2 כוסות אורז/פסטה/בטטה + ירקות.")
    st.write(f"🍌 **לפני אימון:** בננה או 3 תמרים לאנרגיה מתפרצת.")
    st.write(f"🥩 **אחרי אימון (חשוב!):** מנת חלבון + פחמימה זמינה (אורז/תפו״א) להתאוששות.")
    st.info(f"המטרה: להגיע ל-{round(plan['cal'])} קלוריות ו-{round(plan['prot'])} גרם חלבון.")

st.divider()

# --- 5. תוכנית אימונים, משקלים ויומן ביצוע ---
st.subheader("💪 תוכנית אימון ויומן ביצוע")

st.markdown('<div class="custom-box"><strong>📈 חוק ההתקדמות:</strong> אם הצלחת לבצע את כל החזרות בקלות, באימון הבא הוסף 2.5 ק"ג למשקל העבודה.</div>', unsafe_allow_html=True)

workout_data = [
    {"name": "סקוואט (Squat)", "sets": 3, "reps": "8-12", "ratio": 0.5, "steps": ["פיסוק ברוחב כתפיים", "גב ישר וחזה מורם", "ירידה עד שהירכיים מקבילות לרצפה", "דחיפה חזקה מהעקבים"]},
    {"name": "לחיצת חזה (Bench Press)", "sets": 3, "reps": "8-12", "ratio": 0.4, "steps": ["שכיבה על הספסל, עיניים מתחת למוט", "אחיזה רחבה מעט מהכתפיים", "הורדה למרכז החזה בשליטה", "דחיפה מעלה עד לנעילה"]},
    {"name": "מתח / פולי עליון", "sets": 3, "reps": "10-12", "ratio": 0.35, "steps": ["אחיזה רחבה", "משיכת המוט/הגוף לכיוון חזה עליון", "כיווץ חזק של השכמות בשיא", "חזרה איטית ומבוקרת"]}
]

performed = []
for ex in workout_data:
    suggested = round(weight * ex['ratio'] / 2.5) * 2.5
    with st.expander(f"🏋️ {ex['name']}"):
        st.write("**שלבי ביצוע:**")
        for s in ex['steps']: st.write(f"- {s}")
        st.write(f"**יעד אישי:** {ex['sets']} סטים X {ex['reps']} חזרות")
        
        col_w, col_r = st.columns(2)
        w_lifted = col_w.number_input(f"משקל (ק״ג)", key=f"w_{ex['name']}", value=float(suggested), step=2.5)
        r_done = col_r.number_input(f"חזרות", key=f"r_{ex['name']}", value=10, step=1)
        
        performed.append({"תאריך": datetime.now().strftime("%d/%m/%Y"), "תרגיל": ex['name'], "משקל (ק״ג)": w_lifted, "חזרות": r_done})

st.divider()

# --- 6. סיכום, יומן ושמירה ---
if st.button("סכם אימון וחתום יומן"):
    st.balloons()
    df_current = pd.DataFrame(performed)
    
    st.subheader("📋 יומן ביצוע אישי - מה עשינו היום")
    st.table(df_current)
    
    # יצירת קובץ CSV להורדה ושמירה אצל המשתמש
    csv = df_current.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 הורד יומן אימונים למכשיר",
        data=csv,
        file_name=f"workout_{datetime.now().strftime('%d_%m_%Y')}.csv",
        mime="text/csv",
    )
    
    st.success("האימון תועד בהצלחה! המשך לעקוב אחרי המשקלים כדי להבטיח התקדמות.")
