import streamlit as st

# --- הגדרות מיתוג ---
st.set_page_config(
    page_title="Omer's Fitness", 
    layout="centered", 
    page_icon="🏋️" 
)

# עיצוב נקי
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stMetricValue"] { font-size: 1.8rem; color: #CCFF00; }
    .stExpander { border: 1px solid #CCFF00; border-radius: 10px; margin-bottom: 10px; }
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# --- מנוע סגמנטציה וחישוב ---
def analyze_user(w, h, a, act):
    bmi = w / ((h/100) ** 2)
    bmr = (10 * w) + (6.25 * h) - (5 * a) + 5
    tdee = bmr * act
    
    if bmi < 18.5:
        return {"bmi": round(bmi, 1), "status": "אקטומורף (תת-משקל)", "strategy": "מסה אגרסיבית", "cal": round(tdee + 500), "prot": round(w * 2.2)}
    elif 18.5 <= bmi < 25:
        return {"bmi": round(bmi, 1), "status": "מזומורף (תקין)", "strategy": "מסה נקייה", "cal": round(tdee + 300), "prot": round(w * 2.0)}
    else:
        return {"bmi": round(bmi, 1), "status": "אנדומורף (מעל הממוצע)", "strategy": "חיטוב ובניית שריר", "cal": round(tdee - 100), "prot": round(w * 2.4)}

st.markdown("<h1 style='text-align: center; color: #CCFF00;'>OMER'S FITNESS</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 נתוני לקוח")
    age = st.number_input("גיל", 12, 90, 18)
    height = st.number_input("גובה (ס״מ)", 120, 230, 175)
    weight = st.number_input("משקל (ק״ג)", 30, 200, 65)
    activity = st.select_slider("רמת פעילות", options=[1.2, 1.375, 1.55, 1.725], value=1.55)

plan = analyze_user(weight, height, age, activity)

st.divider()
st.subheader("📊 אבחון המערכת")
c1, c2, c3 = st.columns(3)
c1.metric("BMI", plan['bmi'])
c2.metric("יעד קלורי", f"{plan['cal']}")
c3.metric("חלבון יומי", f"{plan['prot']}g")
st.info(f"אסטרטגיה מומלצת: **{plan['strategy']}**")

st.divider()

# --- תוכנית אימונים מפורטת ---
st.subheader("💪 המאמן האישי: הוראות ביצוע")

exercises = [
    {
        "name": "סקוואט (Squat)", 
        "target": "רגליים וישבן", 
        "steps": [
            "1. עמוד בפיסוק ברוחב הכתפיים, בהונות פונות מעט החוצה.",
            "2. שמור על גב ישר וחזה מורם.",
            "3. רד לאט כאילו אתה מתיישב על כיסא דמיוני.",
            "4. דחף מהעקבים וחזור לעמידה."
        ],
        "tip": "אל תיתן לברכיים לקרוס פנימה!"
    },
    {
        "name": "לחיצת חזה (Bench Press)", 
        "target": "חזה ויד אחורית", 
        "steps": [
            "1. שכב על הספסל כשהעיניים בדיוק מתחת למוט.",
            "2. אחוז במוט רחב מעט מרוחב הכתפיים.",
            "3. הורד את המוט לאט למרכז החזה.",
            "4. דחף את המוט בחוזקה עד לנעילת מרפקים."
        ],
        "tip": "שמור את השכמות צמודות לספסל לאורך כל התנועה."
    },
    {
        "name": "מתח (Pull-ups) / פולי עליון", 
        "target": "גב רחב ויד קדמית", 
        "steps": [
            "1. אחוז במוט באחיזה רחבה.",
            "2. משוך את החזה לכיוון המוט תוך כדי הצמדת השכמות.",
            "3. רד לאט ובשליטה עד ליישור ידיים.",
            "4. הימנע משימוש בתנופה של הרגליים."
        ],
        "tip": "תחשוב על למשוך עם המרפקים כלפי מטה, לא עם הידיים."
    }
]

for ex in exercises:
    with st.expander(f"🏋️ {ex['name']} - {ex['target']}"):
        st.write("**שלבי ביצוע:**")
        for step in ex['steps']:
            st.write(step)
        st.warning(f"💡 **טיפ מאמן:** {ex['tip']}")
        st.number_input(f"משקל עבודה (ק״ג)", key=f"rec_{ex['name']}", step=2.5)

st.divider()
st.subheader("🎵 מוזיקת מוטיבציה")
st.markdown('<iframe src="https://open.spotify.com/embed/playlist/37i9dQZF1DX70UOzfvYubW" width="100%" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>', unsafe_allow_html=True)
