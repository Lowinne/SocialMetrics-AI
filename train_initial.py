from database.db_manager import DatabaseManager
from models.sentiment_model import SentimentModel
import config
import traceback

def main():
    db = DatabaseManager(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
    
    print("1. Vérification et configuration de la base de données MySQL...")
    if not db.setup_database():
        print("Arrêt : Impossible de configurer la base de données. Vérifiez config.py et assurez-vous que MySQL tourne.")
        return

    print("2. Récupération des données d'entraînement...")
    raw_data = db.fetch_all_tweets()
    
    if not raw_data:
        print("La base de données est vide. Insertion de quelques tweets de test...")
        test_tweets = [
            ("I love this product, it is absolutely amazing!", 1, 0),
            ("This is the worst service ever, I hate it.", 0, 1),
            ("The movie was okay, nothing special but not bad.", 0, 0),
            ("Super fast delivery, highly recommend!", 1, 0),
            ("Horrible experience, completely broken on arrival.", 0, 1)
        ]
        for t, p, n in test_tweets:
            db.save_annotated_tweet(t, p, n)
        raw_data = db.fetch_all_tweets()

    # Sécurité supplémentaire au cas où l'insertion échoue
    if not raw_data:
        print("Erreur : Aucune donnée disponible même après la tentative d'insertion.")
        return

    print("3. Extraction des features pour scikit-learn...")
    texts = [row['text'] for row in raw_data]
    pos_labels = [row['positive'] for row in raw_data]
    neg_labels = [row['negative'] for row in raw_data]

    print(f"4. Entraînement en cours sur {len(texts)} tweets...")
    model = SentimentModel()
    model.train(texts, pos_labels, neg_labels)

    print("5. Test rapide de prédiction...")
    test_phrase = "This is brilliant, I am so happy!"
    score = model.predict_score(test_phrase)
    print(f"-> Résultat pour '{test_phrase}' : {score}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\nUne erreur inattendue est survenue :")
        traceback.print_exc()