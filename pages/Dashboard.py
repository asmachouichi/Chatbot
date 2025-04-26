import streamlit as st
import altair as alt
import pandas as pd
import ollama
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("🚫 Vous devez être connecté pour accéder au tableau de bord.")
    st.stop()

st.title("⚙️ Tableau de bord")

# Résumé humeur
st.subheader("📊 Humeur")
if "mood_log" in st.session_state and st.session_state["mood_log"]:
    # Organiser les données pour Altair
    dates, moods = zip(*st.session_state["mood_log"])
    df = pd.DataFrame({"Date": dates, "Humeur": moods})

    # Créer un graphique avec Altair
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('Date:T', title='Date'),
        y=alt.Y('Humeur:Q', title='Niveau d’humeur'),
        tooltip=['Date', 'Humeur']
    ).properties(width="container", height=400)

    st.altair_chart(chart, use_container_width=True)
else:
    st.info("Aucune donnée d’humeur pour le moment.")

# Affirmation
st.subheader("🌟 Dernière affirmation")
affirmation = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": "Give me a positive affirmation"}])
st.write(affirmation['message']['content'])

# Résumé journal
st.subheader("📝 Dernière note du journal")
if "journal_entries" in st.session_state and st.session_state["journal_entries"]:
    last_entry = st.session_state["journal_entries"][-1]
    st.markdown(f"**{last_entry[0]}**\n\n{last_entry[1]}")
else:
    st.info("Aucune entrée de journal pour l’instant.")
