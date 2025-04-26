import streamlit as st
import ollama
from database import add_user, check_user

st.set_page_config(page_title="Chatbot Santé Mentale", layout="centered")

# --- Ajouter Bootstrap CSS ---
def load_bootstrap():
    st.markdown(
        """
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { font-family: 'Arial', sans-serif; }
            .container-custom {
                background-color: rgba(255, 255, 255, 0.85);
                padding: 2rem;
                border-radius: 20px;
                max-width: 850px;
                margin: auto;
                margin-top: 3rem;
            }
            .stButton>button {
                margin-top: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

load_bootstrap()

# --- Fond principal sans image (dégradé moderne) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%);
        background-attachment: fixed;
        background-size: cover;
    }
    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(8px);
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Boîte principale ---
st.markdown("<div class='container-custom'>", unsafe_allow_html=True)

# Authentification
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.title("🧠 Chatbot de Santé Mentale")
    st.write("""
        Bienvenue sur notre application de **santé mentale intelligente** !  
        Discutez avec notre **chatbot bienveillant**, recevez des **affirmations positives**, suivez des **guides de méditation**,  
        et découvrez des **conseils pour prendre soin de votre bien-être mental** 💖
    """)

    st.subheader("Connexion 🔐")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if not username or not password:
            st.warning("Veuillez remplir tous les champs de connexion ⚠️")
        elif check_user(username, password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Connexion réussie ✅")
            st.rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect ❌")

    if st.button("Créer un compte 🆕"):
        st.session_state["show_signup"] = True

    if st.session_state.get("show_signup", False):
        st.subheader("Créer un compte")
        new_username = st.text_input("Nouveau nom d'utilisateur")
        new_password = st.text_input("Nouveau mot de passe", type="password")

        if st.button("S'inscrire"):
            if not new_username or not new_password:
                st.warning("Veuillez remplir tous les champs d'inscription ⚠️")
            elif len(new_username) < 4:
                st.warning("Le nom d'utilisateur doit contenir au moins 4 caractères")
            elif len(new_password) < 8:
                st.warning("Le mot de passe doit contenir au moins 8 caractères")
            elif add_user(new_username, new_password):
                st.success("Compte créé avec succès ! Connectez-vous.")
                st.session_state["show_signup"] = False
            else:
                st.error("Ce nom d'utilisateur est déjà utilisé ❌")

else:
    st.title(f"Bienvenue, {st.session_state['username']} ! 🤗")

    if st.button("Se déconnecter"):
        st.session_state["logged_in"] = False
        st.rerun()

    st.session_state.setdefault('conversation_history', [])

    def generate_response(user_input):
        st.session_state['conversation_history'].append({"role": "user", "content": user_input})
        response = ollama.chat(model="llama3.1:8b", messages=st.session_state['conversation_history'])
        ai_response = response['message']['content']
        st.session_state['conversation_history'].append({"role": "assistant", "content": ai_response})
        return ai_response

    def generate_affirmation():
        return ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": "Give me a positive affirmation"}])['message']['content']

    def generate_meditation_guide():
        return ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": "Provide a guided meditation"}])['message']['content']

    def generate_stress_management_tips():
        return ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": "Give stress management tips"}])['message']['content']

    st.subheader("💬 Chat avec l'Assistant")
    for msg in st.session_state['conversation_history']:
        role = "👤 Vous" if msg['role'] == "user" else "🤖 AI"
        st.markdown(f"**{role}:** {msg['content']}")

    user_message = st.text_input("Comment puis-je vous aider aujourd’hui ?")

    if user_message:
        with st.spinner("Réflexion en cours... 💭"):
            ai_response = generate_response(user_message)
            st.markdown(f"**🤖 AI:** {ai_response}")

    st.subheader("🧘 Outils Bien-être")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🌟 Affirmation positive"):
            st.markdown(f"**🌟 Affirmation :** {generate_affirmation()}")

        if st.button("🧘 Méditation guidée"):
            st.markdown(f"**🧘 Méditation :** {generate_meditation_guide()}")

    with col2:
        if st.button("🧘‍♂️ Conseils bien-être"):
            st.markdown(f"**🧘‍♂️ Conseils :** {generate_stress_management_tips()}")

        if st.button("🧠 Stratégies d’adaptation"):
            tips = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": "Give me coping strategies for mental health"}])
            st.markdown(f"**🧠 Stratégies :** {tips['message']['content']}")

        if st.button("💖 Soins personnels"):
            care = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": "Give me self-care advice for mental health"}])
            st.markdown(f"**💖 Soins :** {care['message']['content']}")

st.markdown("</div>", unsafe_allow_html=True)
