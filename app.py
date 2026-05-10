import streamlit as st

# --- 1. הגדרות מיתוג ומראה מקצועי ---
st.set_page_config(
    page_title="Omer's Fitness", 
    layout="centered", 
    page_icon="🏋️" 
)

# עיצוב CSS למראה אפליקציה נקייה ומקצועית
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stMetricValue"] { font-size: 1.8rem; color: #CCFF00; }
    .stExpander { border: 1px solid #CCFF00; border-radius: 10px; margin-bottom: 10px; }
    div.stButton > button:first-child {
        background-color: #CCFF00;
        color: black;
        font-weight: bold;
        border-radius: 20px;
        width: 100%;
    }
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# --- 2. מנוע סגמנטציה וחישוב AI ---
def analyze_user(w, h, a, act):
    # חישוב BMI
    bmi = w / ((h/100) ** 2)
    # חישוב TDEE (הוצאה קלורית יומית)
    bmr = (10 * w) + (6.25 * h) - (5 * a) + 5
    tdee = bmr * act
    
    # סגמנטציה והתאמת אסטרטגיה לפי BMI
    if bmi < 18.5:
        status = "אקטומורף (תת-משקל)"
        strategy = "מסה אגרסיבית - דגש על עודף קלורי גבוה"
        target_cal = tdee + 500
        protein = w * 2.2
        workout_note = "מיקוד בתרגילים מורכבים עם משקלים כבדים ומנוחות ארוכות."
    elif 18.5 <= bmi < 25:
        status = "מזומורף (משקל תקין)"
        strategy = "מסה נקייה - בניית שריר איכותית עם מינימום שומן"
        target_cal = tdee + 300
        protein = w * 2.0
        workout_note = "שילוב של כוח ונפח אימון (Hypertrophy)."
    else:
        status = "אנדומורף (מעל הממוצע)"
        strategy = "חיטוב ובניית שריר במקביל (Body Recomp)"
        target_cal = tdee - 100
        protein = w * 2.4
        workout_note = "נפח גבוה, מנוחות קצרות ודגש על אינטנסיביות."
        
    return {
        "bmi": round(bmi, 1),
        "status": status,
        "strategy": strategy,
        "cal": round(target_cal),
        "prot": round(protein),
        "note": workout_note
    }

# --- 3. ממשק משתמש (UI) ---
st.markdown("<h1 style='text-align: center; color: #CCFF00;'>OMER'S FITNESS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>מערכת AI להתאמת אימונים ותזונה על בסיס נתונים אישיים</p>", unsafe_allow_html=True)

# סרגל צד להזנת נתונים
with st.sidebar:
    st.header("📋 נתוני לקוח")
    age = st.number_input("גיל", 12, 90, 18)
    height = st.number_input("גובה (ס״מ)", 120, 230, 175)
    weight = st.number_input("משקל (ק״ג)", 30, 200, 65)
    activity = st.select_slider("רמת פעילות גופנית", 
                               options=[1.2, 1.375, 1.55, 1.725], 
                               value=1.55,
                               format_func=lambda x: "נמוכה" if x==1.2 else "בינונית" if x==1.55 else "גבוהה")

# הרצת הניתוח
plan = analyze_user(weight, height, age, activity)

# תצוגת האבחון
st.divider()
st.subheader("📊 אבחון המערכת וסגמנטציה")
c1, c2, c3 = st.columns(3)
c1.metric("BMI", plan['bmi'])
c2.metric("יעד קלורי", f"{plan['cal']}")
c3.metric("חלבון יומי", f"{plan['prot']}g")

st.info(f"**סטטוס:** {plan['status']}\n\n**אסטרטגיה:** {plan['strategy']}")
st.write(f"💡 **דגש לאימון:** {plan['note']}")

st.divider()

# --- 4. תוכנית אימונים מפורטת (הדרכה יד ביד) ---
st.subheader("💪 המאמן האישי: הנחיות ביצוע")

workout_data = [
    {
        "name": "סקוואט (Squat)",
        "target": "רגליים וישבן",
        "steps": [
            "1. עמוד בפיסוק ברוחב הכתפיים, בהונות פונות מעט החוצה.",
            "2. שמור על גב ישר, חזה מורם ומבט קדימה.",
            "3. רד לאט עם הישבן לאחור עד שהירכיים מקבילות לרצפה.",
            "4. דחף חזק דרך העקבים וחזור לעמידה."
        ],
        "tip": "אל תיתן לברכיים לקרוס פנימה - דחף אותן החוצה בזמן הירידה."
    },
    {
        "name": "לחיצת חזה (Bench Press)",
        "target": "חזה, כתפיים ויד אחורית",
        "steps": [
            "1. שכב על הספסל כשהעיניים ממוקמות מתחת למוט.",
            "2. אחוז במוט רחב מעט מרוחב הכתפיים.",
            "3. הורד את המוט בצורה מבוקרת למרכז החזה.",
            "4. דחף את המוט למעלה עד לנעילת מרפקים."
        ],
        "tip": "הצמד את השכמות והישבן לספסל לאורך כל התנועה."
    },
    {
        "name": "מתח (Pull-ups) / פולי עליון",
        "target": "גב רחב ויד קדמית",
        "steps": [
            "1. אחוז במוט באחיזה רחבה.",
            "2. משוך את הגוף למעלה (או את הידית) עד שהסנטר מעל המוט.",
            "3. כווץ את השכמות חזק בנקודת השיא.",
            "4. רד לאט עד ליישור מלא של הזרועות."
        ],
        "tip": "תחשוב על משיכת המרפקים לכיוון הרצפה, לא משיכה עם כפות הידיים."
    }
]

for item in workout_data:
    with st.expander(f"🏋️ {item['name']} - {item['target']}"):
        st.write("**שלבי ביצוע:**")
        for step in item['steps']:
            st.write(step)
        st.warning(f"💡 **טיפ מאמן:** {item['tip']}")
        st.write("**פרוטוקול:** 3 סטים X 8-12 חזרות")
        # הזנת משקל עבודה לתיעוד
        st.number_input(f"משקל עבודה ל-{item['name']} (ק״ג)", key=f"input_{item['name']}", step=2.5)

st.divider()

# --- 5. סיכום אימון ---
if st.button("סיום אימון ושמירת נתונים"):
    st.balloons()
    st.success("האימון הושלם בהצלחה! צא לאכול ארוחה עשירה בחלבון ופחמימות.")
