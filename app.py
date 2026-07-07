from flask import Flask, request, jsonify
from models.sentiment_model import SentimentModel
from database.db_manager import DatabaseManager
import config

app = Flask(__name__)

# Initialisation du modèle et de la base de données
# Le modèle va tenter de charger automatiquement les fichiers .joblib s'ils existent
model = SentimentModel()
db = DatabaseManager(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    """
    Endpoint POST pour analyser les sentiments d'une liste de tweets.
    Attend un JSON : { "tweets": ["tweet1", "tweet2", ...] }
    """
    # 1. Gestion des erreurs : Vérification du format global de la requête
    if not request.is_json:
        return jsonify({"error": "Le corps de la requête doit être au format JSON."}), 400
    
    data = request.get_json()
    
    if 'tweets' not in data:
        return jsonify({"error": "La clé 'tweets' est manquante dans le JSON."}), 400
    
    tweets_list = data['tweets']
    
    # 2. Gestion des erreurs : Cas des listes vides ou mauvais types
    if not isinstance(tweets_list, list):
        return jsonify({"error": "Le champ 'tweets' doit être un tableau (liste).Format attendu: string[]"}), 400
        
    if len(tweets_list) == 0:
        return jsonify({"error": "La liste de tweets fournie est vide."}), 400

    # Vérification que tous les éléments de la liste sont bien des chaînes de caractères
    if not all(isinstance(tweet, str) for tweet in tweets_list):
        return jsonify({"error": "Tous les éléments de la liste 'tweets' doivent être des chaînes de caractères."}), 400

    # 3. Vérification de l'état du modèle
    if not model.is_trained:
        return jsonify({"error": "Le modèle d'analyse de sentiments n'est pas encore prêt ou entraîné."}), 503

    # 4. Traitement et calcul des scores
    response_data = {}
    for tweet in tweets_list:
        # Nettoyage rapide des espaces avant/après
        cleaned_tweet = tweet.strip()
        if cleaned_tweet:
            # Calcul du score via notre modèle (-1 à 1)
            score = model.predict_score(cleaned_tweet)
            response_data[tweet] = score
        else:
            response_data[tweet] = 0.0 # Score neutre pour un tweet vide au sein d'une liste

    # 5. Retour de la réponse structurée en JSON
    return jsonify(response_data), 200

if __name__ == '__main__':
    # Lancement de l'application en mode debug pour le développement
    app.run(host='0.0.0.0', port=5000, debug=True)