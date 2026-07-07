import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Chemins de sauvegarde des artefacts du modèle
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.joblib")
POS_MODEL_PATH = os.path.join(MODEL_DIR, "logistic_pos.joblib")
NEG_MODEL_PATH = os.path.join(MODEL_DIR, "logistic_neg.joblib")

class SentimentModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.model_pos = LogisticRegression(max_iter=1000)
        self.model_neg = LogisticRegression(max_iter=1000)
        self.is_trained = False
        self.load_models()

    def load_models(self):
        """Charge les modèles s'ils ont déjà été entraînés et sauvegardés."""
        if (os.path.exists(VECTORIZER_PATH) and 
            os.path.exists(POS_MODEL_PATH) and 
            os.path.exists(NEG_MODEL_PATH)):
            
            self.vectorizer = joblib.load(VECTORIZER_PATH)
            self.model_pos = joblib.load(POS_MODEL_PATH)
            self.model_neg = joblib.load(NEG_MODEL_PATH)
            self.is_trained = True
            print("Modèles de sentiment chargés avec succès.")
        else:
            print("Aucun modèle pré-entraîné trouvé. Un entraînement est requis.")

    def train(self, tweets_text, labels_pos, labels_neg):
        """
        Entraîne le vectoriseur TF-IDF et les deux régression logistiques.
        Conforme aux exigences d'entraînement sur la table tweets.
        """
        if not tweets_text:
            raise ValueError("Le jeu de données d'entraînement ne peut pas être vide.")

        # 1. Vectorisation du texte
        X = self.vectorizer.fit_transform(tweets_text)

        # 2. Entraînement des deux modèles indépendants
        self.model_pos.fit(X, labels_pos)
        self.model_neg.fit(X, labels_neg)
        self.is_trained = True

        # 3. Sauvegarde des artefacts pour l'API et le réentraînement
        joblib.dump(self.vectorizer, VECTORIZER_PATH)
        joblib.dump(self.model_pos, POS_MODEL_PATH)
        joblib.dump(self.model_neg, NEG_MODEL_PATH)
        print("Modèles entraînés et sauvegardés localement.")

    def predict_score(self, tweet_text):
        """
        Calcule un score de sentiment entre -1 (très négatif) et 1 (très positif).
        Calcul basé sur les probabilités des deux classes.
        """
        if not self.is_trained:
            raise Exception("Le modèle n'a pas encore été entraîné.")

        # Transformation du texte via le vectoriseur chargé
        X_vect = self.vectorizer.transform([tweet_text])

        # Récupération des probabilités d'appartenir à la classe 1 (positif ou négatif)
        # predict_proba renvoie [[prob_classe_0, prob_classe_1]]
        prob_pos = self.model_pos.predict_proba(X_vect)[0][1]
        prob_neg = self.model_neg.predict_proba(X_vect)[0][1]

        # Logique du score : si très positif -> tend vers 1, si très négatif -> tend vers -1
        # On fait la différence des forces des probabilités
        score = prob_pos - prob_neg

        # Sécurité pour contraindre strictement le score entre -1 et 1
        return max(-1.0, min(1.0, float(score)))