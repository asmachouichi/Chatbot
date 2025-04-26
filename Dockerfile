# 1. Image de base
FROM python:3.10-slim

# 2. Dossier de travail dans le conteneur
WORKDIR /app

# 3. Copier les fichiers dans le conteneur
COPY . .

# 4. Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# 5. Ouvrir le port de Streamlit
EXPOSE 8501

# 6. Lancer l'application
CMD ["streamlit", "run", "app.py"]

