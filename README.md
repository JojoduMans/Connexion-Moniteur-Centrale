# 🔧 Guide de Diagnostic Réseau CI (Centrale d'Interphonie)

Application interactive de diagnostic réseau pour les Centrales d'Interphonie (port 24005).

## 📋 Description

Cette application Streamlit fournit un guide de diagnostic étape par étape pour résoudre les problèmes de connectivité entre les moniteurs et la centrale d'interphonie. Elle couvre tous les aspects du diagnostic réseau, de la couche physique à la couche applicative.

## ✨ Fonctionnalités

- ✅ Diagnostic séquentiel des couches réseau (OSI)
- ✅ Guide d'analyse Wireshark avec filtres spécifiques
- ✅ Collecte d'informations réseau (IP, VLAN, etc.)
- ✅ Recommandations contextuelles selon les problèmes détectés
- ✅ Export du rapport de diagnostic en JSON
- ✅ Interface utilisateur intuitive avec Streamlit

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation locale

```bash
# Cloner le repository
git clone https://github.com/votre-username/diagnostic-ci-reseau.git
cd diagnostic-ci-reseau

# Créer un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

## 🌐 Déploiement sur Streamlit Cloud

1. Forkez ce repository sur votre compte GitHub
2. Allez sur [share.streamlit.io](https://share.streamlit.io)
3. Connectez-vous avec votre compte GitHub
4. Cliquez sur "New app"
5. Sélectionnez ce repository
6. Choisissez `app.py` comme fichier principal
7. Cliquez sur "Deploy"

## 📖 Utilisation

1. Lancez l'application
2. Suivez les étapes de diagnostic dans l'ordre
3. Répondez aux questions pour chaque étape
4. Collectez les informations réseau demandées
5. Consultez les recommandations adaptées à votre situation
6. Exportez le rapport de diagnostic si nécessaire

## 🔍 Étapes de Diagnostic

1. **Configuration Initiale** : Vérification du label et assignation du moniteur
2. **Découverte LLDP** : Identification de la topologie réseau
3. **Couche Physique** : Vérification du câblage et des LEDs
4. **Couche IP** : Configuration réseau et routage
5. **Connectivité** : Tests ping et traceroute
6. **Port CI (24005)** : Vérification du service et handshake TCP
7. **Couche Applicative** : État du service et logs
8. **Multicast** : Trafic de découverte automatique
9. **QoS** : Priorisation et marquage DSCP

## 📚 Documentation Technique

### Port CI par défaut
- **Port TCP** : 24005
- **Protocole** : TCP
- **Direction** : Moniteur → Centrale

### Commandes Réseau Utiles

**Test de connectivité :**
```bash
ping <ip_centrale>
tracert <ip_centrale>
```

**Analyse de port :**
```bash
netstat -an | grep 24005
telnet <ip_centrale> 24005
```

**Wireshark - Filtres essentiels :**
```
tcp.port == 24005
tcp.port == 24005 and tcp.flags.syn == 1
ip.dst >= 224.0.0.0 and ip.dst <= 239.255.255.255
```

## 🐛 Dépannage

### L'application ne démarre pas
- Vérifiez que toutes les dépendances sont installées : `pip install -r requirements.txt`
- Vérifiez votre version de Python : `python --version` (minimum 3.8)

### Erreur d'import
- Assurez-vous d'être dans le bon répertoire
- Vérifiez que `app.py` et `diagnostic_ci.py` sont présents

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Ouvrir une issue pour signaler un bug
- Proposer des améliorations via une pull request
- Partager vos retours d'expérience

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👤 Auteur

Créé pour faciliter le diagnostic réseau des installations CI.

## 📞 Support

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Consultez la documentation Wireshark : https://www.wireshark.org/docs/
- Documentation réseau Cisco : https://www.cisco.com/

## 🔄 Changelog

### Version 1.0.0 (2025-09-29)
- Version initiale
- Diagnostic complet des 9 étapes
- Interface Streamlit
- Export JSON des rapports
