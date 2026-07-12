# SocialMetrics AI - API d'Analyse de Sentiments

Ce projet propose une API REST développée avec Flask permettant d'évaluer le sentiment des opinions exprimées sur X (anciennement Twitter). Il s'inscrit dans le cadre du développement d'un service pour l'entreprise fictive SocialMetrics AI.

Le modèle de Machine Learning sous-jacent est basé sur une Régression Logistique (Scikit-learn)et renvoie un score de sentiment compris entre -1 (très négatif) et 1 (très positif).

## Lancement via Docker 

Pour garantir une portabilité totale et éviter toute installation locale de Python ou de MySQL, ce projet est entièrement conteneurisé.

### Prérequis Docker
- **Docker** et **Docker Compose** installés sur votre machine.
- Le port `5000` et `3306` doivent être libres.

### Exécution pas à pas

**1, Cloner le dépôt et se placer dans le dossier**
```bash
git clone https://github.com/Lowinne/SocialMetrics-AI.git
cd SocialMetrics-AI
```

**2. Récupérer l'image officielle du projet :**
Ouvrez votre terminal et exécutez :
```bash
docker pull lowinne/socialmetrics-api:latest
```
(Lien du repository : hub.docker.com/r/lowinne/socialmetrics-api)

**3. Lancer l'infrastructure (API + Base de données)**
Placez-vous à la racine du projet et exécutez la commande suivante pour construire et démarrer les conteneurs en arrière-plan :
```bash
docker-compose up -d
```
Docker va automatiquement initialiser MySQL, construire l'environnement Python, et lier les deux services.

**4. Initialiser la BDD et entraîner le modèle**

Une fois les conteneurs lancés, le modèle d'analyse a besoin d'être entraîné sur la base de données (qui vient d'être instanciée de manière vierge). Exécutez le script d'initialisation à l'intérieur du conteneur de l'API :
```bash
docker-compose exec api python train_initial.py
```
Ce script va créer la table tweets, y insérer un jeu de données de test, entraîner la Régression Logistique et générer les fichiers .joblib.
Si erreur MYSQL sur PC, attendre 15s et réessayer 

**5. Redémarrer l'API pour charger le modèle**

```bash
docker-compose restart api
```
### Tester l'API
L'API est maintenant prête à écouter sur le port local 5000. Vous pouvez tester l'endpoint POST /analyze avec la commande suivante :
Sur Mac / Linux :
```bash
curl -X POST http://localhost:5000/analyze \
     -H "Content-Type: application/json" \
     -d '{"tweets": ["I love this product, it is absolutely amazing!", "This service is completely broken and terrible."]}'
```
Sur Windows (Invite de commandes) :
```bash
curl -X POST http://localhost:5000/analyze -H "Content-Type: application/json" -d "{\"tweets\": [\"I love this product, it is absolutely amazing!\", \"This service is completely broken and terrible.\"]}"
```
Réponse attendue (JSON) :
```json
{
  "I love this product, it is absolutely amazing!": 0.19350942371498797,
  "This service is completely broken and terrible.": -0.16453513182458895
}
```
### Générer le Rapport d'Évaluation
Pour afficher les matrices de confusion et les rapports de classification (Précision, Rappel, F1-Score) directement depuis le conteneur, exécutez :
```bash
docker-compose exec api python generate_report_data.py
```
### Arrêter les services
```bash
docker-compose down
```
