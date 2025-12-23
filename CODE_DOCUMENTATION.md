# Documentation Complète du Projet EPL Stats

## Vue d'ensemble du projet

Ce projet est une application de gestion et d'analyse des données d'un établissement d'enseignement supérieur (EPL - École Polytechnique de Lomé). Il permet de générer des données fictives d'étudiants, de les analyser et de les visualiser via un dashboard interactif Streamlit.

## Structure du projet

```
epl_stats/
├── main.py                 # Script principal en ligne de commande
├── run.py                  # Lanceur de l'application
├── README.md              # Documentation du projet
├── requirements.txt       # Dépendances Python
├── setup.sh              # Script d'installation (Linux/Mac)
├── data/                 # Données du projet
│   ├── raw/             # Données brutes
│   └── processed/       # Données traitées
├── notebooks/           # Notebooks Jupyter pour l'exploration
├── outputs/             # Sorties générées (visualisations, exports)
└── src/                 # Code source principal
    ├── __init__.py      # Module Python
    ├── data_loader.py   # Chargement des données
    ├── data_generator.py # Génération de données fictives
    ├── data_analyzer.py  # Analyse statistique
    ├── data_visualizer.py # Création de visualisations
    └── dashboard.py     # Interface web Streamlit
```

---

## Fichiers à la racine

### main.py
**Rôle** : Script principal en ligne de commande pour l'analyse des données EPL.

**Fonctionnalités principales** :
- Chargement et nettoyage des données
- Calculs statistiques détaillés
- Affichage formaté des résultats dans le terminal
- Génération de rapports textuels

**Fonctions clés** :
- `format_number()` : Formatage des nombres avec séparateurs de milliers
- `display_table()` : Affichage de tableaux formatés avec tabulate
- `display_comparison_table()` : Affichage de comparaisons entre groupes
- `display_student_ranking()` : Classement des étudiants
- `main()` : Fonction principale orchestrant toutes les analyses

### run.py
**Rôle** : Script de lancement de l'application avec configuration d'encodage.

**Particularités** :
- Configuration spéciale pour Windows (encodage UTF-8)
- Gestion des erreurs d'encodage
- Import et exécution de main.py

### README.md
**Rôle** : Documentation du projet avec instructions d'installation et d'usage.

**Contenu** :
- Instructions d'installation des dépendances
- Commandes pour générer les données
- Lancement de l'application et du dashboard
- Description de la méthode de génération des données

### requirements.txt
**Rôle** : Liste des dépendances Python du projet.

**Dépendances principales** :
- pandas, numpy : Manipulation de données
- streamlit : Interface web
- plotly : Visualisations interactives
- faker : Génération de données fictives
- scikit-learn : Algorithmes de machine learning
- fpdf : Génération de PDF

---

## Dossier src/ - Code source

### __init__.py
**Rôle** : Fichier vide marquant le dossier comme module Python.

### data_loader.py
**Rôle** : Classe responsable du chargement et du nettoyage des données.

**Classe DataLoader** :
- `__init__(file_path)` : Initialisation avec le chemin du fichier
- `load_data()` : Chargement du CSV avec gestion d'erreurs
- `clean_data()` : Nettoyage complet des données :
  - Suppression des doublons
  - Gestion des valeurs manquantes
  - Conversion des types de données
  - Filtrage des notes invalides (0-20)
  - Ajout de colonnes calculées (moyennes, réussite)

### data_generator.py
**Rôle** : Génération de données fictives réalistes pour l'établissement EPL.

**Classe DataGenerator** :
- **Structure académique** : Définition des départements, filières, UEs et matières
- **Génération d'étudiants** : Création d'étudiants avec caractéristiques réalistes
- **Assignation déterministe** : Filières assignées de manière cohérente par département
- **Système d'enseignants** : Distribution équilibrée avec contraintes (max 5 matières, min 45 étudiants)
- **Génération de notes** : Notes réalistes avec facteurs influençant (niveau individuel, département, matière)

**Méthodes principales** :
- `select_departement()` : Sélection du département selon différentes méthodes
- `generate_etudiant()` : Création d'un étudiant complet
- `generate_notes_etudiant()` : Génération de toutes les notes d'un étudiant
- `setup_teacher_assignments()` : Configuration équilibrée des enseignants
- `generate_dataset()` : Génération du dataset complet

### data_analyzer.py
**Rôle** : Analyses statistiques et calculs sur les données EPL.

**Classe DataAnalyzer** :
- **Statistiques de base** : Moyennes, médianes, écarts-types
- **Analyses par groupes** : Comparaisons par département, filière, UE, matière, enseignant
- **Classements** : Top étudiants, statistiques par groupes
- **Métriques de réussite** : Taux de réussite par différents critères

**Méthodes principales** :
- `calculate_basic_statistics()` : Statistiques globales
- `compare_groups()` : Comparaisons par catégories
- `get_student_ranking()` : Classement des étudiants
- `calculate_success_rate()` : Calcul des taux de réussite

### data_visualizer.py
**Rôle** : Création de visualisations pour les analyses EPL.

**Classe DataVisualizer** :
- **Graphiques Plotly** : Histogrammes, barres, scatter plots
- **Visualisations interactives** : Avec filtres et zooms
- **Exports** : Sauvegarde en HTML, PNG, PDF

**Méthodes principales** :
- `create_histogram()` : Histogrammes de distribution
- `create_bar_chart()` : Graphiques en barres
- `create_scatter_plot()` : Nuages de points
- `create_comparison_charts()` : Comparaisons multiples
- `export_visualization()` : Export des graphiques

### dashboard.py
**Rôle** : Interface web interactive Streamlit pour l'exploration des données EPL.

**Classe StreamlitDashboard** :
- **Interface multi-onglets** :
  - Vue d'ensemble : Métriques générales et KPIs
  - Analyses détaillées : Comparaisons par groupes
  - Classements : Top étudiants et départements
  - Enseignants : Gestion et statistiques des enseignants
  - Données brutes : Exploration des données
  - Qualité des données : Contrôles et métriques
  - Export : Téléchargement de rapports

- **Filtres dynamiques** : Par département, filière, année d'étude
- **Génération de PDF** : Bulletins individuels des étudiants
- **Visualisations interactives** : Graphiques Plotly intégrés

**Fonctionnalités avancées** :
- Cache intelligent pour les performances
- Gestion d'état Streamlit
- Téléchargements de fichiers
- Interface responsive

---

## Dossier data/ - Données

### data/raw/
**Contenu** : Données brutes générées ou importées.
- `notes_epl.csv` : Dataset principal avec toutes les notes des étudiants

### data/processed/
**Contenu** : Données traitées et nettoyées.
- Fichiers CSV transformés et prêts pour l'analyse

---

## Dossier notebooks/ - Exploration

### notebooks/explorations.ipynb
**Rôle** : Notebook Jupyter pour l'exploration interactive des données.

**Contenu** :
- Chargement et exploration initiale des données
- Analyses statistiques de base
- Tests de modèles de machine learning

---

## Dossier outputs/ - Sorties générées

### outputs/visualizations/
**Contenu** : Graphiques et visualisations exportées.
- Fichiers HTML interactifs
- Images PNG/PDF des graphiques

### outputs/statistiques/
**Contenu** : Fichiers CSV des statistiques calculées.
- `classement_etudiants.csv`
- `statistiques_departements.csv`
- `taux_reussite_filieres.csv`

---

## Flux de données

1. **Génération** : `data_generator.py` crée des données fictives réalistes
2. **Chargement** : `data_loader.py` importe et nettoie les données
3. **Analyse** : `data_analyzer.py` calcule les statistiques
4. **Visualisation** : `data_visualizer.py` crée les graphiques
5. **Interface** : `dashboard.py` présente tout dans une interface web
6. **Exploration** : `main.py` permet l'analyse en ligne de commande

## Modèles de données

### Structure d'un étudiant
```python
{
    'ID_Etudiant': 'ETU0001',
    'Nom': 'Dupont',
    'Prenom': 'Jean',
    'Departement': 'Génie Informatique',
    'Grade': 'Licence professionnelle',
    'Annee_etude': 2,
    'Filière': 'IA et Big Data'
}
```

### Structure d'une note
```python
{
    'Code_UE': 'INF2101',
    'Nom_UE': 'Algorithmique Avancée',
    'Code_Matiere': '1INF2101',
    'Matiere': 'Structures de données',
    'Enseignant': 'Dr. Martin',
    'Note_Devoir': 15.5,
    'Note_Examen': 14.2,
    'Note_Finale': 14.8,
    'Coefficient_Devoir': 0.4,
    'Coefficient_Examen': 0.6,
    'Reussite': True
}
```

## Algorithmes utilisés

### Génération de notes
- **Facteurs influençant** : Niveau individuel, difficulté du département, complexité de la matière
- **Distribution normale** : Centrée sur la moyenne avec variance réaliste
- **Contraintes** : Notes entre 0 et 20

### Assignation des enseignants
- **Contraintes** : Maximum 5 matières, minimum 45 étudiants par enseignant
- **Algorithme d'équilibrage** : Distribution basée sur scores composites
- **Optimisation** : Calcul précis du nombre optimal d'enseignants

### Analyses statistiques
- **Métriques descriptives** : Moyennes, médianes, écarts-types

## Technologies utilisées

- **Python 3.8+** : Langage principal
- **Pandas/NumPy** : Manipulation de données
- **Streamlit** : Interface web
- **Plotly** : Visualisations interactives
- **Scikit-learn** : Machine learning
- **FPDF** : Génération de PDF
- **Faker** : Données fictives
- **Jupyter** : Exploration interactive

## Points forts du projet

1. **Données réalistes** : Génération de données cohérentes et représentatives
2. **Interface moderne** : Dashboard Streamlit intuitif et responsive
3. **Analyses complètes** : Couverture exhaustive des métriques académiques
4. **Performance** : Cache intelligent et optimisations
5. **Extensibilité** : Architecture modulaire facile à étendre


*Documentation générée automatiquement - Projet EPL Stats*