-- Création de la base de données si elle n'existe pas
CREATE DATABASE IF NOT EXISTS socialmetrics_db;
USE socialmetrics_db;

-- Création de la table tweets
CREATE TABLE IF NOT EXISTS tweets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    positive TINYINT(1) NOT NULL DEFAULT 0,
    negative TINYINT(1) NOT NULL DEFAULT 0
);