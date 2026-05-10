import streamlit as st

# --- הגדרות מיתוג ---
st.set_page_config(
    page_title="Omer's Fitness", 
    layout="centered", 
    page_icon="🏋️" 
)

hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stMetricValue"] { font-size: 1.8rem; color: #CCFF00; }
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# --- מנוע סגמנטציה וחישוב AI ---
def analyze_user(w, h, a, act):
    bmi = w / ((h/100) ** 2)
    bmr = (10 * w) + (6.25 * h) - (5 * a) + 5
    tdee = bmr * act
    
    if bmi < 18.5:
        return {"bmi": round(bmi, 1), "status": "אקטומורף (תת-משקל)", "strategy": "מסה אגרסיבית", "cal": round(tdee + 500), "prot": round(w * 2.2), "color": "#FF4B4B"}
    elif 18.5 <= bmi < 25:
        return {"bmi": round(bmi, 1), "status": "מזומורף (תקין)", "strategy": "מסה נקייה", "cal": round(tdee + 300), "prot": round(w * 2.0), "color": "#CCFF00"}
    else:
        return {"bmi": round(bmi, 1), "status": "אנדומורף (מעל הממוצע)", "strategy": "חיטוב ובניית שריר", "cal": round(tdee - 100), "prot": round(w * 2.4), "color": "#00CCFF"}

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

st.divider()

# --- תוכנית אימונים עם קישורים מעודכנים ---
st.subheader("💪 המאמן האישי: התחלת אימון")

# השתמשתי בקישורים ממאגר Wikimedia Commons שהם יציבים בהרבה
exercises = [
    {
        "name": "סקוואט (Squat)", 
        "target": "רגליים וישבן", 
        "desc": "שמור על גב ישר, רד עד שהירכיים מקבילות לרצפה ודחף מהעקבים.", 
        "img": "https://upload.wikimedia.org/wikipedia/commons/8/82/Squats.gif"
    },
    {
        "name": "לחיצת חזה (Bench Press)", 
        "target": "חזה ויד אחורית", 
        "desc": "הורד את המוט למרכז החזה ודחף בחוזקה למעלה.", 
        "img": "https://upload.wikimedia.org/wikipedia/commons/f/fe/Barbell-bench-press.gif"
    },
    {
        "name": "מתח (Pull-ups)", 
        "target": "גב רחב", 
        "desc": "משוך את הגוף למעלה עד שהסנטר מעל המוט תוך כיווץ שכמות.", 
        "img": "https://upload.wikimedia.org/wikipedia/commons/e/ee/Pullups.gif"
    }
]

for ex in exercises:
    with st.expander(f"🏋️ {ex['name']} - {ex['target']}"):
        st.write(f"**איך לבצע:** {ex['desc']}")
        st.image(ex['img'], use_container_width=True)
        st.number_input(f"משקל עבודה (ק״ג)", key=f"rec_{ex['name']}")

st.divider()
st.subheader("🎵 פלייליסט אימון")
st.markdown('<iframe src="https://open.spotify.com/embed/playlist/37i9dQZF1DX70UOzfvYubW" width="100%" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>', unsafe_allow_html=True)
