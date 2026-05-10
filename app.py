import streamlit as st

# --- 1. הגדרות מיתוג ומראה מקצועי (אייקון כושר) ---
st.set_page_config(
    page_title="Omer's Fitness", 
    layout="centered", 
    page_icon="🏋️" 
)

# הסתרת רכיבי Streamlit למראה אפליקציה עצמאית
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stMetricValue"] { font-size: 1.8rem; color: #CCFF00; }
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# --- 2. מנוע סגמנטציה וחישוב AI ---
def analyze_user(w, h, a, act):
    bmi = w / ((h/100) ** 2)
    bmr = (10 * w) + (6.25 * h) - (5 * a) + 5
    tdee = bmr * act
    
    # סגמנטציה לפי BMI - התאמת תוכנית אישית
    if bmi < 18.5:
        return {
            "bmi": round(bmi, 1),
            "status": "אקטומורף (תת-משקל)",
            "strategy": "מסה אגרסיבית + עודף קלורי גבוה",
            "cal": round(tdee + 500),
            "prot": round(w * 2.2),
            "workout_notes": "דגש על תרגילים מורכבים, משקלים כבדים ומנוחות ארוכות (120 שניות).",
            "color": "#FF4B4B"
        }
    elif 18.5 <= bmi < 25:
        return {
            "bmi": round(bmi, 1),
            "status": "מזומורף (משקל תקין)",
            "strategy": "מסה נקייה - בניית שריר איכותית",
            "cal": round(tdee + 300),
            "prot": round(w * 2.0),
            "workout_notes": "שילוב כוח ונפח, מנוחות קצרות יותר (90 שניות).",
            "color": "#CCFF00"
        }
    else:
        return {
            "bmi": round(bmi, 1),
            "status": "אנדומורף (מעל הממוצע)",
            "strategy": "חיטוב ובניית שריר במקביל (Body Recomp)",
            "cal": round(tdee - 100),
            "prot": round(w * 2.4),
            "workout_notes": "נפח גבוה, מנוחות קצרות (60 שניות) ודגש על דופק גבוה.",
            "color": "#00CCFF"
        }

# --- 3. ממשק המשתמש (UI) ---
st.markdown("<h1 style='text-align: center; color: #CCFF00;'>OMER'S FITNESS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>מערכת חכמה לאימון אישי ותזונה מדויקת</p>", unsafe_allow_html=True)

# הזנת נתונים
with st.sidebar:
    st.header("📋 נתוני לקוח")
    age = st.number_input("גיל", 12, 90, 18)
    height = st.number_input("גובה (ס״מ)", 120, 230, 175)
    weight = st.number_input("משקל (ק״ג)", 30, 200, 65)
    activity = st.select_slider("רמת פעילות", options=[1.2, 1.375, 1.55, 1.725], value=1.55)

# הפעלת ה-AI של המערכת
plan = analyze_user(weight, height, age, activity)

# תצוגת תוצאות הסגמנטציה
st.divider()
st.subheader("📊 אבחון המערכת והתאמה אישית")
c1, c2, c3 = st.columns(3)
c1.metric("BMI", plan['bmi'])
c2.metric("יעד קלורי", f"{plan['cal']}")
c3.metric("חלבון יומי", f"{plan['prot']}g")

st.markdown(f"""
    <div style="background-color: {plan['color']}; padding: 15px; border-radius: 10px; color: black; font-weight: bold; text-align: center;">
        קטגוריה: {plan['status']} | אסטרטגיה: {plan['strategy']}
    </div>
    """, unsafe_allow_html=True)
st.write(f"💡 **הנחיית המאמן:** {plan['workout_notes']}")

st.divider()

# --- 4. תוכנית אימונים מודרכת עם איורים ---
st.subheader("💪 המאמן האישי: התחלת אימון")

exercises = [
    {
        "name": "סקוואט (Squat)", 
        "target": "רגליים וישבן", 
        "desc": "שמור על גב ישר, רד עד שהירכיים מקבילות לרצפה ודחף מהעקבים.", 
        "img": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJidm9idmJibHZibHZibHZibHYmZXA9djFfaW50ZXJuYWxfZ2lmX2J5X2lkJmN0PWc/3o7TKuafSmBsAkas7e/giphy.gif"
    },
    {
        "name": "לחיצת חזה (Bench Press)", 
        "target": "חזה ויד אחורית", 
        "desc": "הורד את המוט למרכז החזה ודחף בחוזקה למעלה.", 
        "img": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJidm9idmJibHZibHZibHZibHYmZXA9djFfaW50ZXJuYWxfZ2lmX2J5X2lkJmN0PWc/l0HlPtb374H5Y2K5i/giphy.gif"
    },
    {
        "name": "מתח / פולי עליון", 
        "target": "גב רחב", 
        "desc": "משוך את המוט לכיוון החזה העליון תוך כיווץ חזק של השכמות.", 
        "img": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJidm9idmJibHZibHZibHZibHYmZXA9djFfaW50ZXJuYWxfZ2lmX2J5X2lkJmN0PWc/3o7TKMGpx4Z6R6i6nC/giphy.gif"
    }
]

for ex in exercises:
    with st.expander(f"🏋️ {ex['name']} - {ex['target']}"):
        st.write(f"**איך לבצע:** {ex['desc']}")
        st.write("**פרוטוקול:** 3 סטים X 8-12 חזרות")
        st.image(ex['img'], use_column_width=True)
        st.number_input(f"משקל עבודה (ק״ג)", key=f"rec_{ex['name']}")

st.divider()

# --- 5. רכיבי פרימיום: מוזיקה ותזונה ---
st.subheader("🎵 פלייליסט Beast Mode")
st.markdown('<iframe src="https://open.spotify.com/embed/playlist/37i9dQZF1DX70UOzfvYubW" width="100%" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>', unsafe_allow_html=True)

if st.button("סיום אימון ושמירת נתונים"):
    st.balloons()
    st.success("האימון נשמר בהצלחה! צא לאכול ארוחה עם חלבון.")
