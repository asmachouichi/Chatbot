import streamlit as st
from fpdf import FPDF
from datetime import datetime

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("🚫 Vous devez être connecté pour accéder au journal.")
    st.stop()

st.title("📝 Journal personnel")

entry = st.text_area("Écrivez votre pensée du jour 🧠", height=200)

if "journal_entries" not in st.session_state:
    st.session_state["journal_entries"] = []

if st.button("💾 Enregistrer"):
    st.session_state["journal_entries"].append((datetime.now().strftime("%Y-%m-%d %H:%M"), entry))
    st.success("Note enregistrée !")

if st.session_state["journal_entries"]:
    st.subheader("📖 Historique")
    for date, note in st.session_state["journal_entries"]:
        st.markdown(f"**{date}**\n\n{note}")
        st.markdown("---")

    if st.button("📄 Exporter en PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for date, note in st.session_state["journal_entries"]:
            pdf.multi_cell(0, 10, f"{date}\n{note}\n\n")
        pdf.output("journal.pdf")
        with open("journal.pdf", "rb") as f:
            st.download_button("Télécharger le PDF 🧾", f, file_name="journal.pdf")
