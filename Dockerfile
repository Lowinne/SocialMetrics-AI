# Utiliser une image Python officielle légère
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier d'abord les dépendances pour optimiser le cache Docker
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le reste du projet dans le conteneur
COPY . .

# Exposer le port sur lequel l'API va tourner
EXPOSE 5000

# Commande par défaut au lancement du conteneur
CMD ["python", "app.py"]