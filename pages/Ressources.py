import streamlit as st
import ollama

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("🚫 Vous devez être connecté pour accéder aux ressources.")
    st.stop()

st.title("📚 Ressources personnalisées")

mood_level = st.slider("Quel est votre niveau d’humeur actuel ?", 0, 10, 5)

prompt = f"Recommande-moi des articles ou vidéos pour une humeur de niveau {mood_level}"

if st.button("🎯 Rechercher"):
    with st.spinner("Recherche en cours..."):
        response = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": prompt}])
        st.markdown("### 🔍 Suggestions")
        st.markdown(response['message']['content'])
