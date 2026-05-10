import streamlit as st

# --- 1. הגדרות מיתוג ומראה מקצועי ---
st.set_page_config(page_title="Omer's Fitness", layout="centered", page_icon="🏋️")

hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stMetricValue"] { font-size: 1.8rem; color: #CCFF00; }
    .stExpander { border: 1px solid #CCFF00; border-radius: 10px; margin-bottom: 10px; }
    div.stButton > button:first-child {
        background-color: #CCFF00; color: black; font-weight: bold; border-radius: 20px; width: 100%;
    }
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# --- 2. מנוע סגמנטציה וחישוב AI ---
def analyze_user(w, h, a, act):
    bmi = w / ((h/100) ** 2)
    bmr = (10 * w) + (6.25 * h) - (5 * a) + 5
    tdee = bmr * act
    
    if bmi < 18.5:
        status, strategy, target_cal, protein = "אקטומורף (תת-משקל)", "מסה אגרסיבית", tdee + 500, w * 2.2
    elif 18.5 <= bmi < 25:
        status, strategy, target_cal, protein = "מזומורף (תקין)", "מסה נקייה", tdee + 300, w * 2.0
    else:
        status, strategy, target_cal, protein = "אנדומורף (מעל הממוצע)", "חיטוב ובניית שריר", tdee - 100, w * 2.4
        
    return {"bmi": round(bmi, 1), "status": status, "strategy": strategy, "cal": round(target_cal), "prot": round(protein)}

# --- 3. ממשק משתמש ---
st.markdown("<h1 style='text-align: center; color: #CCFF00;'>OMER'S FITNESS</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 נתוני לקוח")
    age = st.number_input("גיל", 12, 90, 18)
    height = st.number_input("גובה (ס״מ)", 120, 230, 175)
    weight = st.number_input("משקל (ק״ג)", 30, 200, 65)
    activity = st.select_slider("רמת פעילות", options=[1.2, 1.375, 1.55, 1.725], value=1.55)

plan = analyze_user(weight, height, age, activity)

# תצוגת אבחון
st.divider()
st.subheader("📊 אבחון AI וסגמנטציה")
c1, c2, c3 = st.columns(3)
c1.metric("BMI", plan['bmi'])
c2.metric("יעד קלורי", f"{plan['cal']}")
c3.metric("חלבון יומי", f"{plan['prot']}g")
st.info(f"**סטטוס:** {plan['status']} | **אסטרטגיה:** {plan['strategy']}")

st.divider()

# --- 4. תוכנית אימונים עם חישוב משקלים ועומס פרוגרסיבי ---
st.subheader("💪 תוכנית אימונים: משקלי עבודה והתקדמות")

# הסבר על עומס פרוגרסיבי
st.markdown("""
<div style="background-color: #333; padding: 15px; border-radius: 10px; border-left: 5px solid #CCFF00;">
    <strong>📈 איך להתקדם?</strong><br>
    אם הצלחת לבצע את כל החזרות בכל הסטים באותו משקל - באימון הבא עליך להוסיף 1.25-2.5 ק"ג לכל צד של המוט. 
    זהו הסוד לבניית שריר!
</div>
""", unsafe_allow_html=True)

workout_data = [
    {
        "name": "סקוואט (Squat)",
        "ratio": 0.5, # מתחילים ב-50% ממשקל הגוף
        "steps": ["פיסוק ברוחב כתפיים", "גב ישר וחזה מורם", "ירידה עד מקביל לרצפה", "דחיפה מהעקבים"],
        "tip": "דחוף ברכיים החוצה בירידה."
    },
    {
        "name": "לחיצת חזה (Bench Press)",
        "ratio": 0.4, # מתחילים ב-40% ממשקל הגוף
        "steps": ["שכיבה על הספסל", "אחיזה רחבה מהכתפיים", "הורדה למרכז החזה", "דחיפה מעלה"],
        "tip": "שמור שכמות צמודות לספסל."
    },
    {
        "name": "מתח / פולי עליון",
        "ratio": 0.35, # מתחילים ב-35% ממשקל הגוף במכשיר
        "steps": ["אחיזה רחבה", "משיכה לחזה עליון", "כיווץ שכמות בשיא", "חזרה איטית"],
        "tip": "משוך עם המרפקים כלפי מטה."
    }
]

for item in workout_data:
    suggested_weight = round(weight * item['ratio'] / 2.5) * 2.5 # עיגול לקפיצות של 2.5 ק"ג
    with st.expander(f"🏋️ {item['name']}"):
        st.write(f"**משקל התחלה מומלץ עבורך:** {suggested_weight} ק״ג")
        st.write("**שלבי ביצוע:**")
        for s in item['steps']: st.write(f"- {s}")
        st.warning(f"💡 {item['tip']}")
        st.write("**פרוטוקול:** 3 סטים X 8-12 חזרות")
        st.number_input(f"כמה הרמת היום? (ק״ג)", key=f"rec_{item['name']}", value=float(suggested_weight), step=2.5)

st.divider()
if st.button("סיום אימון ושמירת נתונים"):
    st.balloons()
    st.success("האימון נשמר! זכור: אם היה קל, באימון הבא מעלים משקל.")
