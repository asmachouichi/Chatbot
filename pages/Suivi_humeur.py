import streamlit as st
import altair as alt
import pandas as pd
from database import save_mood, get_user_moods

st.title("📊 Suivi de l’humeur")

# Vérifie que l'utilisateur est connecté
if "username" not in st.session_state:
    st.error("🚫 Veuillez vous connecter pour accéder à cette page.")
    st.stop()

# Curseur d'humeur
mood = st.slider("Comment vous sentez-vous aujourd’hui ?", 0, 10, 5)

# Champ pour la note
note = st.text_area("Notez quelque chose à propos de votre humeur (facultatif)")

# Sauvegarde de l'humeur
if st.button("💾 Enregistrer l’humeur"):
    if note:  # Si une note est saisie, on l'enregistre
        save_mood(st.session_state["username"], mood, note)
    else:  # Sinon, on enregistre sans note
        save_mood(st.session_state["username"], mood, "Aucune note fournie")
    st.success("✅ Humeur enregistrée avec succès !")

# Récupération des données de l'utilisateur
data = get_user_moods(st.session_state["username"])

# Affichage du graphique si des données existent
if data:
    df = pd.DataFrame(data, columns=["Date", "Humeur", "Note"])
    df["Date"] = pd.to_datetime(df["Date"])

    st.subheader("📈 Évolution de votre humeur")
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X("Date:T", title="Date"),
        y=alt.Y("Humeur:Q", title="Niveau d’humeur"),
        tooltip=["Date", "Humeur"]
    ).properties(
        width="container",
        height=400
    ).interactive()

    st.altair_chart(chart, use_container_width=True)
else:
    st.info("Aucune donnée d’humeur enregistrée pour l’instant.")
