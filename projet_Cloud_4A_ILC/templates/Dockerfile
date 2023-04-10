# Utilisation de l'image de base Nginx
FROM nginx

# Copier le fichier de configuration Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Copier le contenu du dossier templates dans le dossier de travail Nginx
COPY templates/ /usr/share/nginx/html/

# Exposer le port 80 pour les connexions entrantes
EXPOSE 80

# Exécuter Nginx et rediriger les requêtes vers l'application Flask
CMD ["nginx", "-g", "daemon off;"]
