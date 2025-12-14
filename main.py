# main.py
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from tabulate import tabulate

sys.stdout.reconfigure(encoding='utf-8')

# Ajouter le dossier src au chemin
sys.path.append(str(Path(__file__).parent / "src"))

def format_number(value, decimals=2):
    """Formate un nombre avec les décimales appropriées"""
    if isinstance(value, (int, np.integer)):
        return f"{value:,}"
    elif isinstance(value, float):
        return f"{value:.{decimals}f}"
    return str(value)

def display_table(title, data, headers=None):
    """Affiche un tableau formaté dans le terminal"""
    print(f"\n{title}")
    print("=" * 60)
    
    if isinstance(data, dict):
        # Convertir dictionnaire en liste pour tabulate
        table_data = [[key, format_number(value)] for key, value in data.items()]
        print(tabulate(table_data, headers=["Statistique", "Valeur"], tablefmt="grid"))
    elif isinstance(data, pd.DataFrame):
        # Formater les nombres dans le DataFrame
        formatted_df = data.copy()
        for col in formatted_df.columns:
            if pd.api.types.is_numeric_dtype(formatted_df[col]):
                formatted_df[col] = formatted_df[col].apply(lambda x: format_number(x))
        
        print(tabulate(formatted_df, headers='keys', tablefmt='grid', showindex=True))
    elif isinstance(data, pd.Series):
        formatted_series = data.apply(lambda x: format_number(x))
        table_data = [[index, value] for index, value in formatted_series.items()]
        print(tabulate(table_data, headers=[data.name or "Index", "Valeur"], tablefmt="grid"))
    print()

def display_comparison_table(title, comparison_df):
    """Affiche un tableau de comparaison avec mise en forme"""
    print(f"\n{title}")
    print("=" * 80)
    
    # Créer une copie pour la mise en forme
    display_df = comparison_df.copy()
    
    # Formater les colonnes numériques
    for col in display_df.columns:
        if pd.api.types.is_numeric_dtype(display_df[col]):
            if 'Taux' in col or 'Pourcentage' in col or 'réussite' in col.lower():
                display_df[col] = display_df[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "N/A")
            elif 'Note' in col or 'Moyenne' in col or 'moyenne' in col.lower():
                display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "N/A")
            else:
                display_df[col] = display_df[col].apply(lambda x: f"{x:,}" if pd.notnull(x) else "N/A")
    
    print(tabulate(display_df, headers='keys', tablefmt='fancy_grid', showindex=True))
    print()

def display_student_ranking(ranking_df, title="Classement des étudiants"):
    """Affiche le classement des étudiants sous forme de tableau"""
    print(f"\n{title}")
    print("=" * 100)
    
    # Formater le DataFrame
    display_df = ranking_df.copy()
    
    # Formater les colonnes numériques
    for col in display_df.columns:
        if pd.api.types.is_numeric_dtype(display_df[col]):
            if 'Note' in col:
                display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "N/A")
            elif 'Pourcentage' in col or 'Taux' in col:
                display_df[col] = display_df[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "N/A")
    
    # Limiter le nombre de colonnes affichées pour une meilleure lisibilité
    important_cols = ['Nom', 'Prenom', 'Departement', 'Note_Finale', 'Position', 'Rang']
    available_cols = [col for col in important_cols if col in display_df.columns]
    
    if len(available_cols) > 0:
        display_df = display_df[available_cols]
    
    print(tabulate(display_df, headers='keys', tablefmt='fancy_grid', showindex=False))
    print()

def display_summary_table(summary_dict):
    """Affiche le résumé des données sous forme de tableau"""
    print("\n📊 RÉSUMÉ DES DONNÉES")
    print("=" * 60)
    
    # Catégoriser les statistiques
    data_info = {}
    student_info = {}
    performance_info = {}
    
    for key, value in summary_dict.items():
        if 'ligne' in key.lower() or 'colonne' in key.lower():
            data_info[key] = value
        elif 'étudiant' in key.lower() or 'unique' in key.lower():
            student_info[key] = value
        elif 'moyenne' in key.lower() or 'note' in key.lower():
            performance_info[key] = value
        else:
            data_info[key] = value
    
    if data_info:
        print("\n📁 Informations sur les données:")
        table_data = [[k.replace('_', ' ').title(), format_number(v)] for k, v in data_info.items()]
        print(tabulate(table_data, headers=["Information", "Valeur"], tablefmt="simple_grid"))
    
    if student_info:
        print("\n👥 Informations sur les étudiants:")
        table_data = [[k.replace('_', ' ').title(), format_number(v)] for k, v in student_info.items()]
        print(tabulate(table_data, headers=["Information", "Valeur"], tablefmt="simple_grid"))
    
    if performance_info:
        print("\n📈 Indicateurs de performance:")
        table_data = [[k.replace('_', ' ').title(), format_number(v)] for k, v in performance_info.items()]
        print(tabulate(table_data, headers=["Indicateur", "Valeur"], tablefmt="simple_grid"))
    
    print()

def display_department_statistics(dept_stats):
    """Affiche des tableaux détaillés pour chaque département"""
    print("\n" + "=" * 80)
    print("📊 STATISTIQUES DÉTAILLÉES PAR DÉPARTEMENT")
    print("=" * 80)
    
    # Vérifier la structure des données
    if isinstance(dept_stats.columns, pd.MultiIndex):
        # Aplatir les colonnes MultiIndex
        dept_stats.columns = ['_'.join(col).strip() for col in dept_stats.columns.values]
    
    # Extraire les statistiques disponibles
    available_stats = [col for col in dept_stats.columns if 'mean' in col.lower() or 
                      'count' in col.lower() or 'std' in col.lower()]
    
    if not available_stats:
        print("❌ Format de données non supporté")
        return
    
    # Créer un tableau synthétique pour tous les départements
    print("\n📈 COMPARATIF TOUS DÉPARTEMENTS")
    print("-" * 60)
    
    # Tableau comparatif simplifié
    comparative_data = []
    for dept in dept_stats.index:
        row_data = [dept]
        
        # Ajouter les principales métriques
        if 'Note_Finale_mean' in dept_stats.columns:
            moyenne = dept_stats.loc[dept, 'Note_Finale_mean']
            row_data.append(f"{moyenne:.2f}")
        
        if 'Reussite_mean' in dept_stats.columns:
            taux_reussite = dept_stats.loc[dept, 'Reussite_mean'] * 100
            row_data.append(f"{taux_reussite:.1f}%")
        
        if 'ID_Etudiant_nunique' in dept_stats.columns:
            nb_etudiants = dept_stats.loc[dept, 'ID_Etudiant_nunique']
            row_data.append(f"{nb_etudiants:,}")
        
        comparative_data.append(row_data)
    
    # Déterminer les en-têtes
    headers = ["Département"]
    if 'Note_Finale_mean' in dept_stats.columns:
        headers.append("Moyenne")
    if 'Reussite_mean' in dept_stats.columns:
        headers.append("Taux réussite")
    if 'ID_Etudiant_nunique' in dept_stats.columns:
        headers.append("Nb étudiants")
    
    print(tabulate(comparative_data, headers=headers, tablefmt="fancy_grid"))
    
    # Afficher un tableau détaillé pour chaque département
    print("\n" + "=" * 80)
    print("📋 TABLEAUX DÉTAILLÉS PAR DÉPARTEMENT")
    print("=" * 80)
    
    for dept in dept_stats.index:
        print(f"\n🏛️  DÉPARTEMENT: {dept}")
        print("-" * 40)
        
        dept_data = []
        
        # Notes finales
        if 'Note_Finale_mean' in dept_stats.columns:
            moyenne = dept_stats.loc[dept, 'Note_Finale_mean']
            if 'Note_Finale_std' in dept_stats.columns:
                ecart_type = dept_stats.loc[dept, 'Note_Finale_std']
                dept_data.append(["Moyenne notes", f"{moyenne:.2f} ± {ecart_type:.2f}"])
            else:
                dept_data.append(["Moyenne notes", f"{moyenne:.2f}"])
            
            if 'Note_Finale_min' in dept_stats.columns and 'Note_Finale_max' in dept_stats.columns:
                note_min = dept_stats.loc[dept, 'Note_Finale_min']
                note_max = dept_stats.loc[dept, 'Note_Finale_max']
                dept_data.append(["Plage notes", f"{note_min:.1f} - {note_max:.1f}"])
        
        # Taux de réussite
        if 'Reussite_mean' in dept_stats.columns:
            taux = dept_stats.loc[dept, 'Reussite_mean'] * 100
            dept_data.append(["Taux réussite", f"{taux:.1f}%"])
        
        # Effectifs
        if 'ID_Etudiant_nunique' in dept_stats.columns:
            nb_etudiants = dept_stats.loc[dept, 'ID_Etudiant_nunique']
            dept_data.append(["Nombre étudiants", f"{nb_etudiants:,}"])
        
        if 'Note_Finale_count' in dept_stats.columns:
            nb_notes = dept_stats.loc[dept, 'Note_Finale_count']
            dept_data.append(["Nombre notes", f"{nb_notes:,}"])
        
        # Notes de devoir et examen si disponibles
        if 'Note_Devoir_mean' in dept_stats.columns:
            moy_devoir = dept_stats.loc[dept, 'Note_Devoir_mean']
            dept_data.append(["Moyenne devoirs", f"{moy_devoir:.2f}"])
        
        if 'Note_Examen_mean' in dept_stats.columns:
            moy_examen = dept_stats.loc[dept, 'Note_Examen_mean']
            dept_data.append(["Moyenne examens", f"{moy_examen:.2f}"])
        
        # Médiane si disponible
        if 'Note_Finale_median' in dept_stats.columns:
            mediane = dept_stats.loc[dept, 'Note_Finale_median']
            dept_data.append(["Médiane notes", f"{mediane:.2f}"])
        
        print(tabulate(dept_data, headers=["Indicateur", "Valeur"], tablefmt="grid"))
        
        # Calculer et afficher le rang si on a les moyennes
        if 'Note_Finale_mean' in dept_stats.columns:
            # Trier par moyenne décroissante
            classement = dept_stats['Note_Finale_mean'].sort_values(ascending=False)
            rang = list(classement.index).index(dept) + 1
            total = len(classement)
            
            print(f"\n📊 Position: {rang}ème sur {total} départements")
            if rang == 1:
                print("🥇 Premier du classement!")
            elif rang <= 3:
                print("🏆 Dans le top 3!")
            elif rang <= len(classement) // 2:
                print("👍 Au-dessus de la médiane")
        
        print("-" * 40)
    
    # Ajouter un tableau récapitulatif avec classement
    print("\n" + "=" * 80)
    print("🏆 CLASSEMENT FINAL DES DÉPARTEMENTS")
    print("=" * 80)
    
    if 'Note_Finale_mean' in dept_stats.columns and 'Reussite_mean' in dept_stats.columns:
        ranking_data = []
        
        # Créer un DataFrame pour le classement
        ranking_df = pd.DataFrame({
            'Département': dept_stats.index,
            'Moyenne': dept_stats['Note_Finale_mean'],
            'Taux_réussite': dept_stats['Reussite_mean'] * 100
        })
        
        # Ajouter le rang
        ranking_df = ranking_df.sort_values('Moyenne', ascending=False)
        ranking_df['Rang'] = range(1, len(ranking_df) + 1)
        
        # Formater les données pour l'affichage
        for _, row in ranking_df.iterrows():
            ranking_data.append([
                f"{row['Rang']}.",
                row['Département'],
                f"{row['Moyenne']:.2f}",
                f"{row['Taux_réussite']:.1f}%"
            ])
        
        print(tabulate(ranking_data, 
                      headers=["Rang", "Département", "Moyenne", "Taux réussite"], 
                      tablefmt="fancy_grid"))
        
        # Afficher des statistiques globales du classement
        print(f"\n📈 Statistiques du classement:")
        print(f"   • Meilleure moyenne: {ranking_df['Moyenne'].max():.2f} ({ranking_df.iloc[0]['Département']})")
        print(f"   • Plus faible moyenne: {ranking_df['Moyenne'].min():.2f} ({ranking_df.iloc[-1]['Département']})")
        print(f"   • Écart moyen: {ranking_df['Moyenne'].std():.2f} points")
        print(f"   • Différence 1er/dernier: {ranking_df['Moyenne'].max() - ranking_df['Moyenne'].min():.2f} points")

def main():
    print("=" * 60)
    print("SYSTÈME D'ANALYSE DES NOTES - ÉCOLE POLYTECHNIQUE DE LILLE")
    print("=" * 60)

    from src.data_loader import DataLoader
    from src.data_analyzer import DataAnalyzer
    from src.data_visualizer import DataVisualizer
    
    # 1. Charger les données
    print("\n📂 Chargement des données...")
    loader = DataLoader("data/raw/notes_epl.csv")
    df = loader.load_data()
    
    if df is None:
        print("❌ Impossible de charger les données. Arrêt.")
        return
    
    # 2. Nettoyer les données
    print("🧹 Nettoyage des données...")
    df = loader.clean_data()
    summary = loader.get_summary()
    
    if summary:
        display_summary_table(summary)
    
    # 3. Analyser les données
    print("\n📈 Analyse des données...")
    analyzer = DataAnalyzer(df)
    
    # Menu principal
    while True:
        print("\n" + "=" * 40)
        print("MENU PRINCIPAL")
        print("=" * 40)
        print("1. Afficher les statistiques descriptives")
        print("2. Générer des visualisations")
        print("3. Exporter les résultats")
        print("4. Lancer le dashboard interactif (Streamlit)")
        print("5. Analyser les performances par groupe")
        print("6. Quitter")
        
        choix = input("\nVotre choix : ").strip()
        
        if choix == "1":
            # Statistiques descriptives
            stats = analyzer.calculate_basic_statistics()
            
            # Afficher les statistiques globales sous forme de tableau
            display_table("📊 STATISTIQUES GLOBALES", stats['global'])
            
            # Afficher les statistiques par département sous forme de tableau détaillé
            if 'par_departement' in stats:
                dept_stats = stats['par_departement']
                
                # Vérifier le format des données
                if isinstance(dept_stats, pd.DataFrame):
                    # Afficher un tableau complet pour chaque département
                    display_department_statistics(dept_stats)
                else:
                    # Format alternatif si ce n'est pas un DataFrame
                    display_table("🏫 MOYENNES PAR DÉPARTEMENT", dept_stats)
            
            # Afficher les statistiques par UE si disponibles
            if 'par_ue' in stats:
                ue_stats = stats['par_ue']
                if isinstance(ue_stats, pd.DataFrame) and not ue_stats.empty:
                    display_comparison_table("📚 TOP 10 DES UE PAR PERFORMANCE", ue_stats.head(10))
        
        elif choix == "2":
            # Visualisations
            print("\n🎨 Génération des visualisations...")
            visualizer = DataVisualizer(df)
            
            # Sauvegarder les visualisations
            visualizer.export_visualizations()
            print("✅ Visualisations exportées dans outputs/visualizations/")
            
            # Créer un dashboard interactif
            print("🌐 Création du dashboard interactif...")
            fig = visualizer.create_interactive_dashboard()
            fig.write_html("outputs/dashboard_interactif.html")
            print("✅ Dashboard interactif créé: outputs/dashboard_interactif.html")
        
        elif choix == "3":
            # Export des résultats
            print("\n💾 Export des résultats...")
            import os
            output_dir = 'outputs/statistiques'
            os.makedirs(output_dir, exist_ok=True)
            
            # Statistiques par département
            dept_stats = analyzer.compare_groups('Departement')
            dept_stats.to_csv(f'{output_dir}/statistiques_departements.csv')
            display_comparison_table("📊 STATISTIQUES PAR DÉPARTEMENT (Export)", dept_stats)
            
            # Classement des étudiants
            ranking = analyzer.get_student_ranking(100)
            ranking.to_csv(f'{output_dir}/classement_etudiants.csv')
            display_student_ranking(ranking.head(20), "🏆 TOP 20 ÉTUDIANTS")
            
            # Taux de réussite
            success_rates = analyzer.calculate_success_rate('Filière')
            success_rates.to_csv(f'{output_dir}/taux_reussite_filieres.csv')
            display_table("📈 TAUX DE RÉUSSITE PAR FILIÈRE", success_rates)
            
            print("✅ Résultats exportés dans outputs/statistiques/")
        
        elif choix == "4":
            # Lancer Streamlit
            print("\n🚀 Pour lancer le dashboard Streamlit, exécutez:")
            print("   streamlit run src/dashboard.py")
            print("\n🌐 Puis ouvrez votre navigateur à: http://localhost:8501")
            break
        
        elif choix == "5":
            # Analyse par groupe
            print("\n📊 Analyse par groupe:")
            print("  1. Par département")
            print("  2. Par filière")
            print("  3. Par UE")
            print("  4. Par matière")
            print("  5. Par enseignant")
            
            sub_choix = input("\nVotre choix : ").strip()
            
            groups = {
                '1': ('Departement', 'DÉPARTEMENT'),
                '2': ('Filière', 'FILIÈRE'),
                '3': ('Nom_UE', 'UNITÉ D\'ENSEIGNEMENT'),
                '4': ('Matiere', 'MATIÈRE'),
                '5': ('Enseignant', 'ENSEIGNANT')
            }
            
            if sub_choix in groups:
                column, label = groups[sub_choix]
                comparison = analyzer.compare_groups(column)
                
                if not comparison.empty:
                    display_comparison_table(f"📊 COMPARAISON PAR {label}", comparison)
                else:
                    print(f"❌ Aucune donnée disponible pour l'analyse par {label.lower()}")
            else:
                print("❌ Choix invalide. Veuillez choisir entre 1 et 5.")
                
        elif choix == '6':
            print("\n👋 Au revoir !")
            break
        else:
            print("❌ Choix invalide. Veuillez choisir une option entre 1 et 6.")