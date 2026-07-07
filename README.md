# SocialMetrics AI - API d'Analyse de Sentiments

[span_0](start_span)Ce projet propose une API REST développée avec Flask permettant d'évaluer le sentiment des opinions exprimées sur X (anciennement Twitter)[span_0](end_span). [span_1](start_span)Il s'inscrit dans le cadre du développement d'un service pour l'entreprise fictive SocialMetrics AI[span_1](end_span).

[span_2](start_span)Le modèle de Machine Learning sous-jacent est basé sur une Régression Logistique (Scikit-learn)[span_2](end_span) [span_3](start_span)et renvoie un score de sentiment compris entre -1 (très négatif) et 1 (très positif)[span_3](end_span).

## Prérequis

Pour faire tourner ce projet sur votre machine, vous aurez besoin de :
- **Python 3.8+**
- **Un serveur MySQL local actif** (MAMP, WAMP, Docker, ou installation native)

> **Note importante :** L'application est conçue pour être "plug-and-play". [span_4](start_span)[span_5](start_span)Les scripts Python se chargeront automatiquement de créer la base de données et les tables nécessaires[span_4](end_span)[span_5](end_span).

## Installation et Configuration

**1. Cloner le dépôt et se placer dans le dossier**
```bash
git clone <URL_DE_VOTRE_REPO>
cd SocialMetrics-AI
```

**2. Installer les dépendances**
```bash
python3 -m pip install -r requirements.txt
```

**3. Configurer la base de données**
Ouvrez le fichier config.py à la racine du projet et ajustez les identifiants pour qu'ils correspondent à votre serveur MySQL local. Par défaut, la configuration est :
```python
DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = "" # Modifiez ici si votre root possède un mot de passe
DB_NAME = "socialmetrics_db"
```

## Exécution du Projet
**Etape 1 : Initialisation de la BDD et Entraînement du modèle+**
Avant de lancer l'API, il est impératif d'initialiser l'environnement. Exécutez le script suivant :
```bash
python3 train_initial.py
```
Ce script effectue les actions suivantes :
	1.	Connexion au serveur MySQL et création automatique de la base socialmetrics_db et de la table tweets.
	2.	Injection d'un jeu de données de test (si la table est vide).
	3.	Entraînement de la Régression Logistique sur ces données.
	4.	Sauvegarde des modèles sous forme d'artefacts .joblib dans le dossier models/.

**tÉtape 2 : Lancement de l'API Flask+**
Une fois le modèle entraîné, vous pouvez démarrer le serveur local :
```bash
python3 app.py
```
L'API sera accessible sur http://localhost:5000 (ou 8080 selon la configuration du port).

**Étape 3 : Tester l'Endpoint POST**
L'API expose un endpoint POST /analyze qui accepte une liste de tweets.
Ouvrez un nouveau terminal et exécutez la requête suivante :
```bash
curl -X POST http://localhost:5000/analyze \
     -H "Content-Type: application/json" \
     -d '{"tweets": ["I love this product, it is absolutely amazing!", "This service is completely broken and terrible."]}'
```
Réponse attendue (JSON) :
```json
{
  "I love this product, it is absolutely amazing!": 0.5842,
  "This service is completely broken and terrible.": -0.8123
}
```

## Génération du Rapport d'Évaluation
Pour visualiser les performances du modèle (Matrices de confusion, Précision, Rappel, F1-Score), exécutez le script dédié :
```bash
python3 generate_report_data.py
```