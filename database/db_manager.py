import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        self.connection = None

    def setup_database(self):
        """Initialise la BDD et la table automatiquement (Portabilité inter-PC)."""
        try:
            # Connexion générique au serveur (sans préciser la BDD)
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = conn.cursor()
            
            # Création de la base de données si absente
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.execute(f"USE {self.database}")
            
            # Création de la table avec la structure requise
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tweets (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    text TEXT NOT NULL,
                    positive TINYINT(1) NOT NULL DEFAULT 0,
                    negative TINYINT(1) NOT NULL DEFAULT 0
                )
            """)
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Error as e:
            print(f"Erreur SQL lors de l'initialisation : {e}")
            return False

    def connect(self):
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**self.config)
            return self.connection
        except Error as e:
            print(f"Erreur de connexion à MySQL : {e}")
            return None

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def save_annotated_tweet(self, text, positive, negative):
        query = "INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)"
        conn = self.connect()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, (text, positive, negative))
                conn.commit()
                cursor.close()
                return True
            except Error as e:
                print(f"Erreur lors de l'insertion : {e}")
                conn.rollback()
            finally:
                self.disconnect()
        return False

    def fetch_all_tweets(self):
        query = "SELECT text, positive, negative FROM tweets"
        conn = self.connect()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query)
                results = cursor.fetchall()
                cursor.close()
                return results
            except Error as e:
                print(f"Erreur lors de la récupération : {e}")
            finally:
                self.disconnect()
        return []