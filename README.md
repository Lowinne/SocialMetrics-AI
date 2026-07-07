# SocialMetrics AI - API d'Analyse de Sentiments

Ce projet propose une API REST développée avec Flask permettant d'évaluer le sentiment des opinions exprimées sur X (anciennement Twitter). Il s'inscrit dans le cadre du développement d'un service pour l'entreprise fictive SocialMetrics AI.

Le modèle de Machine Learning sous-jacent est basé sur une Régression Logistique (Scikit-learn)et renvoie un score de sentiment compris entre -1 (très négatif) et 1 (très positif).

## Prérequis

Pour faire tourner ce projet sur votre machine, vous aurez besoin de :
- **Python 3.8+**
- **Un serveur MySQL local actif** (MAMP, WAMP, Docker, ou installation native)

## Installation et Configuration

**1. Cloner le dépôt et se placer dans le dossier**
```bash
git clone https://github.com/Lowinne/SocialMetrics-AI.git
cd SocialMetrics-AI
```

**2. Installer les dépendances**
```bash
python3 -m pip install -r requirements.txt
```
ou
```bash
python -m pip install -r requirements.txt
```

**3. Configurer la base de données**
Ouvrez le fichier config.py à la racine du projet et ajustez les identifiants pour qu'ils correspondent à votre serveur MySQL local. Par défaut, la configuration est :
```python
DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = "" 
DB_NAME = "socialmetrics_db"
```

## Exécution du Projet

**Etape 0 : Démarrer le service MySQL selon votre OS ***
Avant d'exécuter l'application, assurez-vous que votre serveur MySQL local est actif. Voici comment le lancer :

#### Sur macOS (via Homebrew)
Si vous avez installé MySQL avec Homebrew, ouvrez votre terminal et exécutez :
```bash
brew install mysql

# Vérifier le statut des services
brew services list

# Démarrer le service MySQL
brew services start mysql
```
#### Sur Windows (PC)
Il faut MySQL d'installer sur le PC
Via l'invite de commandes en mode Administrateur
```bash
net start mysql
```
ou
```bash
net start MySQL80
``` 

**Etape 1 : Initialisation de la BDD et Entraînement du modèle+**
 **Note importante :** Attention Il faut que les informations dans config.py soit bonne !! (DB_USER & DB_PASSWORD)
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