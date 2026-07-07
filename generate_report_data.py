from sklearn.metrics import confusion_matrix, classification_report
from database.db_manager import DatabaseManager
from models.sentiment_model import SentimentModel
import config

def main():
    db = DatabaseManager(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
    model = SentimentModel()
    
    if not model.is_trained:
        print("Erreur : Le modèle doit être entraîné avant de générer le rapport.")
        return

    print("Récupération des données pour l'évaluation...")
    raw_data = db.fetch_all_tweets()
    
    texts = [row['text'] for row in raw_data]
    y_true_pos = [row['positive'] for row in raw_data]
    y_true_neg = [row['negative'] for row in raw_data]

    y_pred_pos = []
    y_pred_neg = []

    print("Génération des prédictions en cours...")
    for text in texts:
        # On utilise directement les modèles sous-jacents pour prédire la classe (0 ou 1)
        X_vect = model.vectorizer.transform([text])
        y_pred_pos.append(model.model_pos.predict(X_vect)[0])
        y_pred_neg.append(model.model_neg.predict(X_vect)[0])

    print("\n" + "="*50)
    print(" MATRICE DE CONFUSION : CLASSE POSITIVE ")
    print("="*50)
    print(confusion_matrix(y_true_pos, y_pred_pos))
    print("\nRapport détaillé (Classe Positive) :")
    print(classification_report(y_true_pos, y_pred_pos, zero_division=0))

    print("\n" + "="*50)
    print(" MATRICE DE CONFUSION : CLASSE NÉGATIVE ")
    print("="*50)
    print(confusion_matrix(y_true_neg, y_pred_neg))
    print("\nRapport détaillé (Classe Négative) :")
    print(classification_report(y_true_neg, y_pred_neg, zero_division=0))

if __name__ == "__main__":
    main()