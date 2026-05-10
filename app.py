import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. הגדרות מיתוג ואייקון (יופיע בשולחן העבודה) ---
st.set_page_config(
    page_title="Omer's Fitness", 
    layout="centered", 
    page_icon="🏋️"
)

# עיצוב CSS מתקדם לסלולרי (רקע שחור, ללא Sidebar)
style = """
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    h1, h2, h3 { color: #CCFF00 !important; text-align: center; }
    [data-testid="stMetricValue"] { color: #CCFF00 !important; text-align: center; }
    
    /* תיבות תוכן */
    .custom-box {
        background-color: #111111; 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid #333333;
        border-right: 5px solid #CCFF00;
        color: #FFFFFF;
        margin-bottom: 20px;
        direction: rtl;
    }
    
    /* כפתורים גדולים ונוחים למגע סלולרי */
    div.stButton > button:first-child {
        background-color: #CCFF00; 
        color: black; 
        font-weight: bold; 
        border-radius: 30px; 
        height: 60px;
        border: none;
        font-size: 1.3rem;
        width: 100%;
        margin-top: 20px;
    }
    
    .stExpander { border: 1px solid #333333; border-radius: 10px; background-color: #0a0a0a; direction: rtl; }
    
    /* התאמת כיוון טקסט לימין */
    .stMarkdown, .stNumberInput, .stSelectSlider { direction: rtl; }
    </style>
"""
st.markdown(style, unsafe_allow_html=True)

# --- 2. מנוע חישוב וסגמנטציה ---
def analyze_user(w, h, a, act):
    bmi = w / ((h/100) ** 2)
    bmr = (10 * w) + (6.25 * h) - (5 * a) + 5
    tdee = bmr * act
    
    if bmi < 18.5:
        status, strategy, cal, prot = "מבנה רזה (Ectomorph)", "מסה אגרסיבית", tdee + 500, w * 2.2
    elif 18.5 <= bmi < 25:
        status, strategy, cal, prot = "מבנה אתלטי (Mesomorph)", "מסה נקייה", tdee + 300, w * 2.0
    else:
        status, strategy, cal, prot = "מבנה רחב (Endomorph)", "חיטוב ובניית שריר", tdee - 100, w * 2.4
        
    return {"bmi": round(bmi, 1), "status": status, "strategy": strategy, "cal": round(cal), "prot": round(prot)}

# --- 3. שלב א: הזנת נתונים (Onboarding) ---
st.markdown("<h1>OMER'S FITNESS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>הזן נתונים כדי להתחיל את האימון</p>", unsafe_allow_html=True)

# שימוש בתיבה מרכזית להזנת נתונים (במקום Sidebar)
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("גיל", 12, 90, 18)
        weight = st.number_input("משקל (ק״ג)", 30, 200, 65)
    with col2:
        height = st.number_input("גובה (ס״מ)", 120, 230, 175)
        activity = st.select_slider("רמת פעילות", options=[1.2, 1.375, 1.55, 1.725], value=1.55)

if st.button("בנה לי תוכנית אימון 🚀"):
    st.session_state.data_submitted = True

# --- שלב ב: הצגת התוכנית (רק אחרי לחיצה) ---
if 'data_submitted' in st.session_state:
    plan = analyze_user(weight, height, age, activity)
    
    st.divider()
    # אבחון
    st.subheader("📊 האבחון שלך")
    c1, c2, c3 = st.columns(3)
    c1.metric("BMI", plan['bmi'])
    c2.metric("קלוריות", f"{plan['cal']}")
    c3.metric("חלבון", f"{plan['prot']}g")
    
    st.markdown(f'<div class="custom-box"><strong>סטטוס:</strong> {plan["status"]}<br><strong>אסטרטגיה:</strong> {plan["strategy"]}</div>', unsafe_allow_html=True)
    
    # תזונה
    st.subheader("🍎 תפריט יומי מומלץ")
    with st.expander("לחץ לצפייה בתפריט"):
        st.write(f"🍳 **בוקר:** חביתה מ-3 ביצים או שייק חלבון עם שיבולת שועל.")
        st.write(f"🍗 **צהריים:** 200ג חזה עוף/בקר + 2 כוסות אורז/פסטה + ירקות.")
        st.write(f"🍌 **לפני אימון:** בננה או תמרים.")
        st.write(f"🥩 **אחרי אימון:** חלבון + פחמימה זמינה להתאוששות.")
        st.info(f"יעד יומי: {plan['cal']} קלוריות | {plan['prot']}ג חלבון")

    st.divider()
    
    # אימונים ויומן
    st.subheader("💪 תוכנית אימון ויומן")
    st.markdown('<div class="custom-box"><strong>📈 טיפ התקדמות:</strong> הצלחת 12 חזרות? באימון הבא תוסיף 2.5 ק"ג.</div>', unsafe_allow_html=True)

    workout_data = [
        {"name": "סקוואט (Squat)", "ratio": 0.5, "steps": ["פיסוק ברוחב כתפיים", "גב ישר", "ירידה עד מקביל", "דחיפה מהעקבים"]},
        {"name": "לחיצת חזה (Bench)", "ratio": 0.4, "steps": ["שכיבה על ספסל", "אחיזה רחבה", "הורדה לחזה", "דחיפה מעלה"]},
        {"name": "מתח / פולי עליון", "ratio": 0.35, "steps": ["אחיזה רחבה", "משיכה לחזה", "כיווץ שכמות", "חזרה איטית"]}
    ]

    performed = []
    for ex in workout_data:
        suggested = round(weight * ex['ratio'] / 2.5) * 2.5
        with st.expander(f"🏋️ {ex['name']}"):
            for s in ex['steps']: st.write(f"- {s}")
            st.write(f"**משקל התחלה מומלץ:** {suggested} ק״ג")
            w_lifted = st.number_input(f"משקל שהורם", key=f"w_{ex['name']}", value=float(suggested), step=2.5)
            r_done = st.number_input(f"חזרות שבוצעו", key=f"r_{ex['name']}", value=10, step=1)
            performed.append({"תרגיל": ex['name'], "משקל": w_lifted, "חזרות": r_done})

    st.divider()
    
    # סיום ושמירה
    if st.button("סכם אימון ושמור ביומן 📋"):
        st.balloons()
        df = pd.DataFrame(performed)
        st.table(df)
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 הורד יומן אימונים", data=csv, file_name=f"workout_{datetime.now().strftime('%d_%m_%Y')}.csv", mime="text/csv")
        st.success("האימון תועד! צא לאכול ותנוח טוב.")
