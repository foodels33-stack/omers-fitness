# --- תפריט מוזיקה מתקדם ---
st.markdown('<div class="fitness-card">', unsafe_allow_html=True)
st.subheader("🎵 פסקול האימון")

music_option = st.radio(
    "בחר אווירה:",
    ["מוזיקה מקורית (Loop)", "רוק (YouTube)", "אלקטרוני (YouTube)"],
    horizontal=True
)

if music_option == "מוזיקה מקורית (Loop)":
    try:
        audio_file = open('workout_track.mp3', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3', loop=True)
        st.caption("מנגן את רצועת הבית של האפליקציה בלולאה")
    except FileNotFoundError:
        st.info("כדי לשמוע את המוזיקה המקורית, העלה קובץ בשם workout_track.mp3 ל-GitHub.")

elif music_option == "רוק (YouTube)":
    # פלייליסט רוק מוטיבציה רשמי
    st.markdown("""
        <iframe width="100%" height="200" src="https://www.youtube.com/embed/5S6p_7q7kEw" 
        frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
    """, unsafe_allow_html=True)

else:
    # פלייליסט אלקטרוני/טראנס אימון רשמי
    st.markdown("""
        <iframe width="100%" height="200" src="https://www.youtube.com/embed/4pD_v_7E60s" 
        frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
