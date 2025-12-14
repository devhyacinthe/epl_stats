# src/dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from pathlib import Path
import sys
import tempfile
import os
import time

sys.stdout.reconfigure(encoding='utf-8')

# Ajouter le chemin du projet
sys.path.append(str(Path(__file__).parent.parent))

from src.data_loader import DataLoader
from src.data_analyzer import DataAnalyzer
from src.data_visualizer import DataVisualizer

class StreamlitDashboard:
    def __init__(self):
        st.set_page_config(
            page_title="Dashboard Notes EPL",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Initialiser les variables de session Si elles n'existent pas
        
        if 'data_loaded' not in st.session_state:
            st.session_state.data_loaded = False
        if 'uploaded_file' not in st.session_state:
            st.session_state.uploaded_file = None
        if 'df' not in st.session_state:
            st.session_state.df = None
        if 'analyzer' not in st.session_state:
            st.session_state.analyzer = None
        if 'visualizer' not in st.session_state:
            st.session_state.visualizer = None
        
        # Initialiser les variables d'instance à partir de session_state
        self.data_loaded = st.session_state.data_loaded
        self.uploaded_file = st.session_state.uploaded_file
        self.df = st.session_state.df
        self.analyzer = st.session_state.analyzer
        self.visualizer = st.session_state.visualizer
    
    def load_data_from_file(self, file_path, file_name):
        """Charge les données depuis un fichier"""
        try:
            # Afficher un spinner pendant le chargement
            with st.spinner(f"Chargement de {file_name}..."):
                data_loader = DataLoader(file_path)
                df = data_loader.load_data()
                
                if df is not None:
                    df = data_loader.clean_data()
                    analyzer = DataAnalyzer(df)
                    visualizer = DataVisualizer(df)
                    
                    # Mettre à jour les variables de session
                    st.session_state.data_loaded = True
                    st.session_state.uploaded_file = file_name
                    st.session_state.df = df
                    st.session_state.analyzer = analyzer
                    st.session_state.visualizer = visualizer
                    
                    # Mettre à jour les variables d'instance
                    self.data_loaded = True
                    self.uploaded_file = file_name
                    self.df = df
                    self.analyzer = analyzer
                    self.visualizer = visualizer
                    
                    st.success(f"✅ Données chargées avec succès : {file_name}")
                    time.sleep(1)  # Pause pour voir le message
                    return True
                else:
                    st.error("❌ Impossible de charger les données depuis le fichier.")
                    return False
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement: {str(e)}")
            return False
    
    def show_file_uploader(self):
        """Affiche l'interface de téléchargement de fichier"""
        st.title("📤 Téléchargement de Fichier CSV")
        st.markdown("---")
        
        # Créer deux onglets pour les options
        tab1, tab2 = st.tabs(["📁 Télécharger votre fichier", "📂 Utiliser le fichier par défaut"])
        
        with tab1:
            st.subheader("Télécharger votre propre fichier CSV")
            uploaded_file = st.file_uploader(
                "Choisissez un fichier CSV",
                type=["csv"],
                help="Le fichier doit contenir les colonnes: ID_Etudiant, Departement, Note_Finale, etc.",
                key="file_uploader"
            )
            
            if uploaded_file is not None:
                # Afficher un aperçu du fichier
                try:
                    # Lire les premières lignes pour prévisualisation
                    preview_df = pd.read_csv(uploaded_file, nrows=5)
                    st.info("Aperçu du fichier (5 premières lignes):")
                    st.dataframe(preview_df)
                    
                    # Afficher les informations du fichier
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Colonnes", len(preview_df.columns))
                    with col2:
                        st.metric("Lignes (preview)", len(preview_df))
                    
                    # Vérifier les colonnes obligatoires
                    required_columns = ['ID_Etudiant', 'Departement', 'Note_Finale', 'Reussite']
                    missing_columns = [col for col in required_columns if col not in preview_df.columns]
                    
                    if missing_columns:
                        st.warning(f"⚠️ Colonnes manquantes dans l'aperçu: {', '.join(missing_columns)}")
                        st.warning("Le fichier pourrait ne pas fonctionner correctement.")
                    else:
                        st.success("✅ Toutes les colonnes obligatoires sont présentes")
                    
                except Exception as e:
                    st.warning(f"Impossible de prévisualiser le fichier: {e}")
                
                # Bouton pour charger le fichier
                if st.button("📂 Charger ce fichier", type="primary", use_container_width=True):
                    # Sauvegarder le fichier temporairement
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    # Charger les données
                    if self.load_data_from_file(tmp_path, uploaded_file.name):
                        # Forcer le rerun
                        st.rerun()
                    
                    # Nettoyer le fichier temporaire
                    try:
                        os.unlink(tmp_path)
                    except:
                        pass
        
        with tab2:
            st.subheader("Utiliser le fichier par défaut")
            default_file = "data/raw/notes_epl.csv"
            
            if os.path.exists(default_file):
                st.success("✅ Fichier par défaut trouvé")
                
                # Afficher les informations du fichier
                file_size = os.path.getsize(default_file) / 1024 / 1024  # En MB
                st.metric("Taille du fichier", f"{file_size:.2f} MB")
                
                # Prévisualiser le fichier
                try:
                    preview_df = pd.read_csv(default_file, nrows=5)
                    st.info("Aperçu du fichier par défaut (5 premières lignes):")
                    st.dataframe(preview_df)
                except:
                    st.info("Impossible de prévisualiser le fichier")
                
                # Bouton pour charger le fichier par défaut
                if st.button("📁 Charger le fichier par défaut", type="primary", use_container_width=True):
                    if self.load_data_from_file(default_file, "notes_epl.csv (par défaut)"):
                        st.rerun()
            else:
                st.error("❌ Fichier par défaut non trouvé")
                st.info("Le fichier par défaut devrait être à l'emplacement: data/raw/notes_epl.csv")
        
        # Instructions
        with st.expander("📋 Format requis du fichier CSV"):
            st.markdown("""
            ### **Format requis pour le fichier CSV**
            
            **Colonnes obligatoires:**
            - `ID_Etudiant` : Identifiant unique de l'étudiant
            - `Departement` : Département (ex: Génie Informatique)
            - `Note_Finale` : Note finale sur 20 (nombre décimal)
            - `Reussite` : Booléen (True/False) ou 0/1
            
            **Colonnes recommandées pour une analyse complète:**
            - `Nom`, `Prenom` : Nom et prénom des étudiants
            - `Filière` : Spécialisation
            - `Code_UE`, `Nom_UE` : Unité d'enseignement
            - `Code_Matiere`, `Matiere` : Matière spécifique
            - `Note_Devoir`, `Note_Examen` : Notes partielles
            - `Annee_etude` : Année d'étude (nombre entier)
            - `Enseignant` : Nom de l'enseignant
            - `Date_Examen`, `Session` : Informations sur l'examen
            
            **Spécifications techniques:**
            - **Encodage:** UTF-8
            - **Séparateur:** Virgule (,)
            - **Décimal:** Point (.)
            - **En-têtes:** Première ligne contient les noms de colonnes
            
            **Exemple de ligne de données:**
            """)
            
            # Exemple de données formaté
            example_data = {
                'ID_Etudiant': 'ETU0001',
                'Nom': 'Dupont',
                'Prenom': 'Jean',
                'Departement': 'Génie Informatique',
                'Filière': 'Génie Logiciel',
                'Annee_etude': 2,
                'Code_UE': 'INF2101',
                'Nom_UE': 'Algorithmique Avancée',
                'Code_Matiere': '1INF2101',
                'Matiere': 'Structures de données avancées',
                'Note_Devoir': 15.5,
                'Note_Examen': 14.0,
                'Note_Finale': 14.7,
                'Reussite': True,
                'Enseignant': 'Prof. Martin',
                'Date_Examen': '2024-01-15',
                'Session': 'Principale'
            }
            
            # Afficher l'exemple sous forme de tableau
            example_df = pd.DataFrame([example_data])
            st.dataframe(example_df)
            
            # Code pour télécharger un exemple
            st.markdown("### **Télécharger un fichier exemple**")
            example_csv = example_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger le fichier exemple",
                data=example_csv,
                file_name="exemple_format_notes.csv",
                mime="text/csv",
                help="Téléchargez cet exemple pour voir le format requis"
            )
    
    def run(self):
        """Exécute le dashboard"""
        # DEBUG: Afficher l'état de session
        # st.write("DEBUG - data_loaded:", st.session_state.data_loaded)
        # st.write("DEBUG - df is None:", self.df is None)
        
        # Vérifier si les données sont chargées
        if not st.session_state.data_loaded or self.df is None:
            self.show_file_uploader()
            return
        
        # Titre principal avec nom du fichier
        st.title(f"📈 Dashboard d'Analyse des Notes")
        st.caption(f"Fichier chargé: {st.session_state.uploaded_file}")
        st.markdown("---")
        
        # Bouton pour changer de fichier dans la sidebar
        with st.sidebar:
            if st.button("🔄 Changer de fichier", use_container_width=True):
                # Réinitialiser l'état
                st.session_state.data_loaded = False
                st.session_state.uploaded_file = None
                st.session_state.df = None
                st.session_state.analyzer = None
                st.session_state.visualizer = None
                st.rerun()
        
        # S'assurer que les variables d'instance sont à jour
        self.df = st.session_state.df
        self.analyzer = st.session_state.analyzer
        self.visualizer = st.session_state.visualizer
        
        if self.df is None or self.analyzer is None:
            st.error("❌ Erreur: Les données ne sont pas correctement chargées")
            if st.button("Réinitialiser et charger un nouveau fichier"):
                st.session_state.clear()
                st.rerun()
            return
        
        # Sidebar avec filtres
        with st.sidebar:
            st.header("🔧 Filtres et Paramètres")
            
            # Afficher les informations du fichier
            with st.expander("📁 Informations du fichier"):
                st.write(f"**Fichier:** {st.session_state.uploaded_file}")
                st.write(f"**Lignes totales:** {len(self.df):,}")
                st.write(f"**Étudiants uniques:** {self.df['ID_Etudiant'].nunique():,}")
                st.write(f"**Colonnes:** {', '.join(self.df.columns.tolist()[:5])}...")
                if 'Note_Finale' in self.df.columns:
                    st.write(f"**Plage des notes:** {self.df['Note_Finale'].min():.1f} - {self.df['Note_Finale'].max():.1f}")
            
            # Filtres multi-sélection
            selected_departements = st.multiselect(
                "Départements",
                options=self.df['Departement'].unique() if 'Departement' in self.df.columns else [],
                default=self.df['Departement'].unique() if 'Departement' in self.df.columns else []
            )
            
            selected_filieres = st.multiselect(
                "Filières",
                options=self.df['Filière'].unique() if 'Filière' in self.df.columns else [],
                default=self.df['Filière'].unique() if 'Filière' in self.df.columns else []
            )
            
            # Filtre par année si la colonne existe
            if 'Annee_etude' in self.df.columns:
                selected_annees = st.multiselect(
                    "Années d'étude",
                    options=sorted(self.df['Annee_etude'].unique()),
                    default=sorted(self.df['Annee_etude'].unique())
                )
            else:
                selected_annees = []
            
            # Slider pour le seuil
            seuil_reussite = st.slider(
                "Seuil de réussite",
                min_value=0.0,
                max_value=20.0,
                value=10.0,
                step=0.5
            )
            
            # Appliquer les filtres
            filtered_df = self.df.copy()
            if selected_departements and 'Departement' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['Departement'].isin(selected_departements)]
            if selected_filieres and 'Filière' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['Filière'].isin(selected_filieres)]
            if selected_annees and 'Annee_etude' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['Annee_etude'].isin(selected_annees)]
            
            # Mettre à jour l'analyseur avec les données filtrées
            self.analyzer.df = filtered_df
            self.visualizer.df = filtered_df
            
            # Métriques dans la sidebar
            st.markdown("---")
            st.header("📊 Métriques")
            
            col1, col2 = st.columns(2)
            with col1:
                if 'Note_Finale' in filtered_df.columns:
                    moyenne = filtered_df['Note_Finale'].mean()
                    st.metric("Moyenne", f"{moyenne:.2f}/20")
                else:
                    st.metric("Moyenne", "N/A")
            
            with col2:
                if 'Note_Finale' in filtered_df.columns:
                    taux_reussite = (filtered_df['Note_Finale'] >= seuil_reussite).mean() * 100
                    st.metric("Taux réussite", f"{taux_reussite:.1f}%")
                else:
                    st.metric("Taux réussite", "N/A")
            
            if 'ID_Etudiant' in filtered_df.columns:
                st.metric("Nombre étudiants", filtered_df['ID_Etudiant'].nunique())
            st.metric("Nombre de notes", len(filtered_df))
        
        # Layout principal avec tabs
        tab_names = ["📊 Vue d'ensemble", "📈 Analyses détaillées", "🏆 Classements", 
                    "📋 Données brutes", "🔍 Qualité des données", "💾 Export"]
        
        # Vérifier quelles onglets sont disponibles
        available_tabs = []
        for tab_name in tab_names:
            available_tabs.append(tab_name)
        
        tabs = st.tabs(available_tabs)
        
        # Afficher chaque onglet
        for i, tab in enumerate(tabs):
            with tab:
                if i == 0:
                    self._show_overview_tab()
                elif i == 1:
                    self._show_analysis_tab()
                elif i == 2:
                    self._show_ranking_tab()
                elif i == 3:
                    self._show_raw_data_tab(filtered_df)
                elif i == 4:
                    self._show_quality_tab()
                elif i == 5:
                    self._show_export_tab(filtered_df)
    
    # ... (les autres méthodes restent les mêmes: _show_overview_tab, _show_analysis_tab, etc.)
    # Gardez toutes les autres méthodes telles quelles, seulement modifiez les références
    # pour utiliser self.df, self.analyzer, etc.

    def _show_overview_tab(self):
        """Affiche l'onglet vue d'ensemble"""
        st.header("Vue d'ensemble des performances")
        
        # Vérifier que les données sont disponibles
        if self.df is None or self.analyzer is None:
            st.error("❌ Données non disponibles")
            return
        
        # Calculer les statistiques de base
        try:
            stats = self.analyzer.calculate_basic_statistics()
            if 'global' not in stats:
                st.error("❌ Impossible de calculer les statistiques")
                return
        except Exception as e:
            st.error(f"❌ Erreur lors du calcul des statistiques: {str(e)}")
            return
        
        # 3 colonnes pour les métriques
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Moyenne", f"{stats['global']['moyenne']:.2f}")
            st.metric("Médiane", f"{stats['global']['mediane']:.2f}")
        
        with col2:
            st.metric("Écart-type", f"{stats['global']['ecart_type']:.2f}")
            st.metric("Minimum", f"{stats['global']['minimum']:.2f}")
        
        with col3:
            st.metric("Maximum", f"{stats['global']['maximum']:.2f}")
            st.metric("Nombre", f"{stats['global']['count']:,}")
        
        # Graphiques principaux
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("Distribution des notes")
            if 'Note_Finale' in self.df.columns:
                fig = px.histogram(self.df, x='Note_Finale', nbins=20,
                                  title='Histogramme des notes finales')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Colonne 'Note_Finale' non trouvée")
        
        with col_chart2:
            st.subheader("Boxplot par département")
            if 'Departement' in self.df.columns and 'Note_Finale' in self.df.columns:
                fig = px.box(self.df, x='Departement', y='Note_Finale',
                            title='Distribution des notes par département')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Colonnes 'Departement' ou 'Note_Finale' non trouvées")
        
        # Taux de réussite par filière
        st.subheader("Taux de réussite par filière")
        if 'Filière' in self.df.columns:
            success_by_filiere = self.analyzer.calculate_success_rate('Filière')
            fig = px.bar(x=success_by_filiere.index, y=success_by_filiere['Taux_reussite'],
                        labels={'x': 'Filière', 'y': 'Taux de réussite (%)'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Colonne 'Filière' non disponible")

    def _show_analysis_tab(self):
        """Affiche l'onglet d'analyse détaillée"""
        st.header("Analyses statistiques détaillées")
        
        # Sélecteur d'analyse
        analysis_type = st.selectbox(
            "Type d'analyse",
            ["Par département", "Par filière", "Par UE", "Par matière", "Par enseignant"]
        )
        
        mapping = {
            "Par département": "Departement",
            "Par filière": "Filière",
            "Par UE": "Nom_UE",
            "Par matière": "Matiere",
            "Par enseignant": "Enseignant"
        }
        
        selected_column = mapping[analysis_type]
        
        # Tableau des statistiques
        comparison = self.analyzer.compare_groups(selected_column)
        st.dataframe(comparison.style.background_gradient(
            subset=['Moyenne_Finale', 'Taux_reussite'],
            cmap='YlOrRd'
        ))
        
        # Graphiques supplémentaires
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"Moyennes par {analysis_type.lower()}")
            fig = px.bar(comparison, x=comparison.index, y='Moyenne_Finale',
                        title=f'Moyennes finales par {analysis_type.lower()}')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader(f"Corrélation Devoir vs Examen")
            fig = px.scatter(self.df, x='Note_Devoir', y='Note_Examen',
                           color=selected_column,
                           title='Relation entre notes de devoir et examen')
            st.plotly_chart(fig, use_container_width=True)
    
    def _show_ranking_tab(self):
        """Affiche l'onglet des classements"""
        st.header("Classements")
        
        top_n = st.slider("Nombre d'étudiants à afficher", 10, 100, 20)
        
        # Classement des étudiants
        st.subheader(f"Top {top_n} étudiants")
        ranking = self.analyzer.get_student_ranking(top_n)
        st.dataframe(ranking)
        
        # Classement des départements
        st.subheader("Classement des départements")
        dept_stats = self.analyzer.compare_groups('Departement')
        dept_stats = dept_stats.sort_values('Moyenne_Finale', ascending=False)
        
        fig = px.bar(dept_stats, x=dept_stats.index, y='Moyenne_Finale',
                    title='Moyenne par département (classement)')
        st.plotly_chart(fig, use_container_width=True)
    
    def _show_raw_data_tab(self, filtered_df):
        """Affiche les données brutes"""
        st.header("Données brutes")
        
        # Recherche et filtrage
        search_term = st.text_input("Rechercher (Nom, Prénom, Matière...)")
        
        if search_term:
            mask = filtered_df.apply(lambda row: row.astype(str).str.contains(
                search_term, case=False).any(), axis=1)
            display_df = filtered_df[mask]
        else:
            display_df = filtered_df
        
        # Pagination
        page_size = st.selectbox("Lignes par page", [10, 25, 50, 100], index=0)
        total_pages = len(display_df) // page_size + 1
        
        page_number = st.number_input("Page", min_value=1, 
                                     max_value=total_pages, value=1)
        
        start_idx = (page_number - 1) * page_size
        end_idx = start_idx + page_size
        
        st.dataframe(display_df.iloc[start_idx:end_idx])
        
        # Statistiques rapides
        with st.expander("Statistiques de la vue actuelle"):
            st.write(f"Nombre de lignes : {len(display_df)}")
            st.write(f"Nombre d'étudiants : {display_df['ID_Etudiant'].nunique()}")
            st.write(f"Moyenne : {display_df['Note_Finale'].mean():.2f}")
    
    def _show_quality_tab(self):
        """Affiche l'onglet qualité des données"""
        st.header("🔍 Qualité des données")
        
        if self.df is None:
            st.warning("Aucune donnée chargée")
            return
        
        # Métriques de qualité
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_rows = len(self.df)
            st.metric("Total lignes", f"{total_rows:,}")
        
        with col2:
            null_count = self.df.isnull().sum().sum()
            null_percent = (null_count / (total_rows * len(self.df.columns)) * 100).round(2)
            st.metric("Valeurs nulles", f"{null_count:,}", f"{null_percent}%")
        
        with col3:
            duplicate_count = self.df.duplicated().sum()
            duplicate_percent = (duplicate_count / total_rows * 100).round(2)
            st.metric("Duplicatas", f"{duplicate_count:,}", f"{duplicate_percent}%")
        
        with col4:
            student_count = self.df['ID_Etudiant'].nunique()
            st.metric("Étudiants uniques", f"{student_count:,}")
        
        # Analyse par colonne
        st.subheader("Analyse détaillée par colonne")
        
        quality_data = []
        for column in self.df.columns:
            col_info = {
                'Colonne': column,
                'Type': str(self.df[column].dtype),
                'Valeurs uniques': self.df[column].nunique(),
                'Valeurs nulles': self.df[column].isnull().sum(),
                '% Nulles': (self.df[column].isnull().sum() / total_rows * 100).round(2),
                'Exemple': str(self.df[column].iloc[0]) if not self.df[column].empty else 'N/A'
            }
            quality_data.append(col_info)
        
        quality_df = pd.DataFrame(quality_data)
        st.dataframe(quality_df)
        
        # Distribution des notes
        st.subheader("Distribution des notes finales")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            fig = px.histogram(self.df, x='Note_Finale', 
                             title="Distribution des notes",
                             labels={'Note_Finale': 'Note finale', 'count': 'Fréquence'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col_chart2:
            # Vérifier les valeurs aberrantes
            Q1 = self.df['Note_Finale'].quantile(0.25)
            Q3 = self.df['Note_Finale'].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = self.df[(self.df['Note_Finale'] < lower_bound) | 
                             (self.df['Note_Finale'] > upper_bound)]
            
            fig = px.box(self.df, y='Note_Finale', 
                        title=f"Boxplot des notes (outliers: {len(outliers)})")
            st.plotly_chart(fig, use_container_width=True)
        
        # Problèmes détectés
        st.subheader("Problèmes détectés")
        
        problems = []
        
        # Vérifier les notes hors limites
        invalid_notes = self.df[(self.df['Note_Finale'] < 0) | (self.df['Note_Finale'] > 20)]
        if len(invalid_notes) > 0:
            problems.append(f"❌ {len(invalid_notes)} notes en dehors de l'intervalle [0, 20]")
        
        # Vérifier les colonnes avec trop de valeurs nulles
        high_null_cols = quality_df[quality_df['% Nulles'] > 50]['Colonne'].tolist()
        if high_null_cols:
            problems.append(f"⚠️ {len(high_null_cols)} colonnes avec plus de 50% de valeurs nulles")
        
        # Vérifier les incohérences dans les taux de réussite
        if 'Reussite' in self.df.columns and 'Note_Finale' in self.df.columns:
            inconsistent = self.df[((self.df['Note_Finale'] >= 10) & (self.df['Reussite'] == False)) |
                                 ((self.df['Note_Finale'] < 10) & (self.df['Reussite'] == True))]
            if len(inconsistent) > 0:
                problems.append(f"❌ {len(inconsistent)} incohérences entre Note_Finale et Reussite")
        
        if problems:
            for problem in problems:
                st.warning(problem)
        else:
            st.success("✅ Aucun problème majeur détecté")
    
    def _show_export_tab(self, filtered_df):
        """Affiche l'onglet d'export"""
        st.header("Export des données et résultats")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("📊 Données")
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="💾 Télécharger CSV",
                data=csv,
                file_name="notes_filtrees.csv",
                mime="text/csv"
            )
        
        with col2:
            st.subheader("📈 Statistiques")
            stats = self.analyzer.calculate_basic_statistics()
            
            # CORRECTION SIMPLIFIÉE
            if 'par_departement' in stats:
                # Créer le DataFrame correctement
                if isinstance(stats['par_departement'], pd.DataFrame):
                    stats_df = stats['par_departement']
                    # Aplatir les colonnes MultiIndex
                    if isinstance(stats_df.columns, pd.MultiIndex):
                        stats_df.columns = ['_'.join(col).strip() for col in stats_df.columns.values]
                else:
                    # Si c'est un dictionnaire
                    stats_df = pd.DataFrame.from_dict(stats['par_departement'], orient='index')
            else:
                stats_df = pd.DataFrame({'Message': ['Statistiques non disponibles']})
            
            csv_stats = stats_df.to_csv().encode('utf-8')
            st.download_button(
                label="📋 Statistiques CSV",
                data=csv_stats,
                file_name="statistiques_departements.csv",
                mime="text/csv"
            )
        
        with col3:
            st.subheader("🎓 Classement")
            ranking = self.analyzer.get_student_ranking(100)
            if ranking is not None and not ranking.empty:
                csv_ranking = ranking.to_csv().encode('utf-8')
                st.download_button(
                    label="🏆 Classement CSV",
                    data=csv_ranking,
                    file_name="classement_etudiants.csv",
                    mime="text/csv"
                )
            else:
                st.info("Classement non disponible")
        
        # Export graphiques
        st.subheader("🖼️ Graphiques")
        
        if st.button("🔄 Générer et exporter tous les graphiques"):
            with st.spinner("Génération des graphiques..."):
                self.visualizer.export_visualizations()
                st.success("✅ Graphiques exportés dans outputs/visualizations/")
        
        # Export Excel complet
        st.subheader("📑 Export Excel Complet")
        
        if st.button("📊 Exporter tout en Excel"):
            with st.spinner("Création du fichier Excel..."):
                try:
                    # Créer un fichier Excel avec plusieurs onglets
                    excel_file = "export_complet_notes.xlsx"
                    
                    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                        # 1. Données filtrées
                        filtered_df.to_excel(writer, sheet_name='Donnees_Filtrees', index=False)
                        
                        # 2. Statistiques
                        stats = self.analyzer.calculate_basic_statistics()
                        
                        # 2.1 Statistiques globales
                        if 'global' in stats:
                            global_stats = pd.DataFrame(
                                list(stats['global'].items()),
                                columns=['Statistique', 'Valeur']
                            )
                            global_stats.to_excel(writer, sheet_name='Stats_Globales', index=False)
                        
                        # 2.2 Statistiques par département
                        if 'par_departement' in stats and stats['par_departement'] is not None:
                            if isinstance(stats['par_departement'], pd.DataFrame):
                                stats_dep = stats['par_departement'].copy()
                                if isinstance(stats_dep.columns, pd.MultiIndex):
                                    stats_dep.columns = ['_'.join(col).strip() for col in stats_dep.columns.values]
                                stats_dep.to_excel(writer, sheet_name='Stats_Departements')
                        
                        # 3. Classement
                        ranking = self.analyzer.get_student_ranking(50)
                        if ranking is not None and not ranking.empty:
                            ranking.to_excel(writer, sheet_name='Top_50', index=False)
                        
                        # 4. Qualité des données
                        quality_data = []
                        for column in self.df.columns:
                            quality_data.append({
                                'Colonne': column,
                                'Type': str(self.df[column].dtype),
                                'Valeurs uniques': self.df[column].nunique(),
                                'Valeurs nulles': self.df[column].isnull().sum(),
                                '% Nulles': (self.df[column].isnull().sum() / len(self.df) * 100).round(2)
                            })
                        
                        quality_df = pd.DataFrame(quality_data)
                        quality_df.to_excel(writer, sheet_name='Qualite_Donnees', index=False)
                    
                    # Télécharger le fichier Excel
                    with open(excel_file, "rb") as f:
                        st.download_button(
                            label="⬇️ Télécharger Excel complet",
                            data=f,
                            file_name=excel_file,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    
                    st.success(f"✅ Fichier Excel créé: {excel_file}")
                    
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'export Excel: {str(e)}")

# Point d'entrée pour Streamlit
def main():
    app = StreamlitDashboard()
    app.run()

if __name__ == "__main__":
    main()