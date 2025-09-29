# Guide de Déploiement

Ce guide vous explique comment déployer l'application sur différentes plateformes.

## 📦 Structure des fichiers pour GitHub

Voici la structure complète à uploader sur GitHub :

```
diagnostic-ci-reseau/
├── .streamlit/
│   └── config.toml
├── app.py
├── diagnostic_ci.py
├── requirements.txt
├── .gitignore
├── README.md
├── LICENSE
├── CONTRIBUTING.md
└── DEPLOY.md
```

## 🚀 Déploiement sur Streamlit Cloud (Recommandé)

### Étape 1 : Préparer le repository GitHub

1. Créez un nouveau repository sur GitHub
2. Clonez-le localement :
   ```bash
   git clone https://github.com/votre-username/diagnostic-ci-reseau.git
   cd diagnostic-ci-reseau
   ```

3. Ajoutez tous les fichiers :
   ```bash
   # Créez le dossier .streamlit
   mkdir .streamlit
   
   # Ajoutez tous les fichiers fournis
   # app.py, diagnostic_ci.py, requirements.txt, etc.
   ```

4. Commitez et poussez :
   ```bash
   git add .
   git commit -m "Initial commit - Application de diagnostic réseau CI"
   git push origin main
   ```

### Étape 2 : Déployer sur Streamlit Cloud

1. Allez sur [share.streamlit.io](https://share.streamlit.io)
2. Connectez-vous avec votre compte GitHub
3. Cliquez sur **"New app"**
4. Remplissez les informations :
   - **Repository** : `votre-username/diagnostic-ci-reseau`
   - **Branch** : `main`
   - **Main file path** : `app.py`
5. Cliquez sur **"Deploy!"**

L'application sera disponible à : `https://votre-username-diagnostic-ci-reseau.streamlit.app`

### Étape 3 : Mises à jour

Pour mettre à jour l'application :
```bash
git add .
git commit -m "Description des changements"
git push origin main
```

Streamlit Cloud redéploiera automatiquement l'application.

## 🐳 Déploiement avec Docker (Alternative)

### Créer un Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Construire et lancer

```bash
# Construire l'image
docker build -t diagnostic-ci .

# Lancer le conteneur
docker run -p 8501:8501 diagnostic-ci
```

Accédez à l'application sur `http://localhost:8501`

## 🌐 Déploiement sur Heroku

### Fichiers nécessaires

**Procfile** :
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**setup.sh** :
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

### Commandes de déploiement

```bash
# Installer Heroku CLI et se connecter
heroku login

# Créer l'application
heroku create diagnostic-ci-reseau

# Déployer
git push heroku main

# Ouvrir l'application
heroku open
```

## 🖥️ Déploiement sur un serveur local

### Installation

```bash
# Cloner le repository
git clone https://github.com/votre-username/diagnostic-ci-reseau.git
cd diagnostic-ci-reseau

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Lancement

```bash
streamlit run app.py
```

L'application sera accessible sur `http://localhost:8501`

### Service systemd (Linux)

Créez `/etc/systemd/system/diagnostic-ci.service` :

```ini
[Unit]
Description=Diagnostic CI Streamlit App
After=network.target

[Service]
Type=simple
User=votre-utilisateur
WorkingDirectory=/chemin/vers/diagnostic-ci-reseau
Environment="PATH=/chemin/vers/venv/bin"
ExecStart=/chemin/vers/venv/bin/streamlit run app.py --server.port=8501

[Install]
WantedBy=multi-user.target
```

Activer et démarrer :
```bash
sudo systemctl enable diagnostic-ci
sudo systemctl start diagnostic-ci
sudo systemctl status diagnostic-ci
```

## 🔒 Sécurité

### Streamlit Cloud
- Activez l'authentification si nécessaire
- Utilisez des secrets pour les données sensibles dans `.streamlit/secrets.toml`

### Serveur local
- Utilisez un reverse proxy (nginx/Apache) avec HTTPS
- Configurez un firewall
- Limitez l'accès par IP si possible

### Exemple nginx

```nginx
server {
    listen 80;
    server_name diagnostic-ci.votre-domaine.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 Monitoring

### Streamlit Cloud
- Consultez les logs dans l'interface Streamlit Cloud
- Activez les analytics si disponibles

### Serveur local
```bash
# Logs en temps réel
journalctl -u diagnostic-ci -f

# Utilisation des ressources
htop
```

## 🐛 Dépannage

### Problème : Application ne démarre pas
```bash
# Vérifier les logs
streamlit run app.py --logger.level=debug
```

### Problème : Erreur de dépendances
```bash
# Réinstaller les dépendances
pip install --force-reinstall -r requirements.txt
```

### Problème : Port déjà utilisé
```bash
# Changer le port
streamlit run app.py --server.port=8502
```

## 📞 Support

Pour toute question sur le déploiement :
- Ouvrez une issue sur GitHub
- Documentation Streamlit : https://docs.streamlit.io/streamlit-cloud
- Documentation Docker : https://docs.docker.com/
