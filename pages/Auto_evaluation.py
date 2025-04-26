import streamlit as st

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("🚫 Vous devez être connecté pour accéder à l’auto-évaluation.")
    st.stop()

st.title("🧪 Auto-évaluation : Stress et Anxiété")

st.subheader("PHQ-9 (Dépression)")
phq_score = sum([st.slider(f"Question {i+1}", 0, 3, 0) for i in range(9)])

st.subheader("GAD-7 (Anxiété)")
gad_score = sum([st.slider(f"Question {i+1}", 0, 3, 0) for i in range(7)])

if st.button("🔎 Évaluer"):
    st.success(f"Score PHQ-9 : {phq_score}/27")
    st.success(f"Score GAD-7 : {gad_score}/21")

    if phq_score >= 15:
        st.warning("⚠️ Symptômes dépressifs modérés à sévères.")
    if gad_score >= 15:
        st.warning("⚠️ Symptômes anxieux modérés à sévères.")
