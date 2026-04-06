# 📊 GROUP 1 DATA APP - Web Scraping & Analytics

Application web interactive de web scraping et d'analyse de données, développée avec Streamlit.

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 Fonctionnalités

- **Web Scraping en temps réel** - Extraction de données depuis un site web sur 3 catégories :
  - Ordinateurs
  - Téléphones
  - TV / Home Cinema

- **Téléchargement de données** - Accès aux datasets pré-scrapés

- **Tableau de bord interactif** - Visualisations et analyses statistiques :
  - Prix moyens par marque
  - Distribution des prix par état (neuf/occasion)
  - Graphiques personnalisés avec Matplotlib & Seaborn

- **Formulaire intégré** - Questionnaire KoboToolbox

---

## 🛠️ Technologies utilisées

| Bibliothèque | Version | Utilisation |
|-------------|---------|-------------|
| Streamlit | 1.28+ | Interface web |
| BeautifulSoup4 | 4.12+ | Parsing HTML |
| Pandas | 2.0+ | Manipulation de données |
| Matplotlib | 3.7+ | Visualisations |
| Seaborn | 0.12+ | Graphiques statistiques |
| Requests | 2.31+ | Requêtes HTTP |


---

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets)

### Étapes d'installation

1. **Cloner le dépôt**
```bash
git clone https://github.com/votre-repo/group1-data-app.git
cd group1-data-app
```

2. **Créer un environnement virtuel** (recommandé)
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Lancer l'application**
```bash
streamlit run group1_data_app.py
```

## 📖 Utilisation

### 1. Web Scraping
- Sélectionnez "Scrape data using BeautifulSoup" dans le menu latéral
- Choisissez le nombre de pages (1-250)
- Cliquez sur la catégorie souhaitée (Ordinateurs/Téléphones/Cinéma)

### 2. Téléchargement des données
- Sélectionnez "Download scraped data"
- Cliquez sur le bouton correspondant à la catégorie

### 3. Dashboard analytique
- Sélectionnez "Dashboard of the data"
- Explorez les visualisations :
  - Prix moyens par marque
  - Distribution des prix selon l'état

## 4. Formulaire
- Sélectionnez "Fill the form"
- Accédez au questionnaire KoboToolbox intégré


## ⚠️ Disclaimer académique 

Ce projet a été réalisé dans le cadre d'un examen en classe (Groupe 1 - Data Science).  
> Il est strictement éducatif et non commercial.  
> Les données sont scrapées à des fins d'apprentissage uniquement.  
> Aucune intention de nuire ou de surcharger les serveurs d'Expat-Dakar.
