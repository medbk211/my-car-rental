# Car Rental Backend 🚗

Bienvenue dans le backend de **Car Rental**, une application de location de voitures développée avec Python et FastAPI. Ce backend gère l'authentification, la gestion des voitures et des réservations.

## 🛠 Technologies utilisées
- **Langage** : Python 🐍
- **Framework** : FastAPI ⚡
- **Base de données** : PostgreSQL 🗄
- **ORM** : SQLAlchemy
- **Migrations** : Alembic
- **Authentification** : OAuth2 & JWT
- **Dockerisation** : Docker 🐳

## 📦 Installation

1. **Cloner le projet** :
   ```sh
   git clone https://github.com/medbk211/car-rental-backend.git
   cd car-rental-backend
   ```

2. **Créer et activer un environnement virtuel** :
   ```sh
   python -m venv venv
   source venv/bin/activate  # Sur macOS/Linux
   venv\Scripts\activate  # Sur Windows
   ```

3. **Installer les dépendances** :
   ```sh
   pip install -r requirements.txt
   ```

4. **Configurer les variables d'environnement** :
   Créer un fichier `.env` et ajouter :
   ```ini
   DATABASE_URL=postgresql://user:password@localhost/car_rental_db
   SECRET_KEY=your_secret_key
   ```

5. **Appliquer les migrations** :
   ```sh
   alembic upgrade head
   ```

6. **Lancer le serveur** :
   ```sh
   uvicorn app.main:app --reload
   ```

Le backend sera accessible sur `http://127.0.0.1:8000` 🚀.



## 🚀 Déploiement avec Docker

1. **Créer l'image Docker** :
   ```sh
   docker build -t car-rental-backend .
   ```
2. **Lancer le conteneur** :
   ```sh
   docker run -p 8000:8000 --env-file .env car-rental-backend
   ```

## 📌 Auteur
Développé par **Mohamed Al Breiki**.

💡 N'hésite pas à contribuer ou à signaler un problème via [GitHub Issues](https://github.com/medbk211/car-rental-backend/issues).

