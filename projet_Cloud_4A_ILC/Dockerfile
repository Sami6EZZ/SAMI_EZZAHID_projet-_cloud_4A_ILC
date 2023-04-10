# Utilisez l'image de base Python
FROM python:3.8-slim-buster

# Mettez à jour le répertoire de travail
WORKDIR /app

# Copiez le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copiez l'ensemble du code source dans le conteneur
COPY . .

# Exposez le port 5000
EXPOSE 5000

# Définissez la commande pour démarrer le serveur Flask
CMD [ "python", "./app.py" ]
