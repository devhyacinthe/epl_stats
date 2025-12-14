import pandas as pd
import numpy as np
from pathlib import Path

class DataLoader:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.data = None
    
    def load_data(self):
        """Charge les données depuis le fichier CSV"""
        try:
            self.data = pd.read_csv(self.file_path, encoding='utf-8')
            print(f"✅ Données chargées : {len(self.data)} lignes, {self.data.shape[1]} colonnes")
            return self.data
        except Exception as e:
            print(f"❌ Erreur lors du chargement : {e}")
            return None
    
    def clean_data(self):
        """Nettoie et prépare les données"""
        if self.data is None:
            print("❌ Aucune donnée à nettoyer")
            return None
        
        # Créer une copie
        df = self.data.copy()
        
        # 1. Supprimer les doublons
        df = df.drop_duplicates()
        print(f"📊 Après suppression des doublons : {len(df)} lignes")
        
        # 2. Vérifier les valeurs manquantes
        missing_values = df.isnull().sum()
        if missing_values.any(): 
            print("⚠️  Valeurs manquantes trouvées :")
            print(missing_values[missing_values > 0]) # Afficher uniquement les colonnes avec des valeurs manquantes
            df = df.dropna()  # Supprimer les lignes avec des valeurs manquantes
        
        # 3. Convertir les types de données
        numeric_columns = ['Note_Devoir', 'Note_Examen', 'Note_Finale']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce') # Convertir en numérique, forcer les erreurs en NaN
        
        # 4. Filtrer les notes invalides
        df = df[(df['Note_Finale'] >= 0) & (df['Note_Finale'] <= 20)] #On ne garde que les notes entre 0 et 20
        
        # 5. Ajouter des colonnes calculées
        if 'Note_Finale' in df.columns:
            df['Reussite_Bool'] = df['Note_Finale'] >= 10
            df['Categorie_Note'] = pd.cut(df['Note_Finale'], 
                                        bins=[0, 8, 10, 12, 14, 16, 20],
                                        labels=['Insuffisant', 'Faible', 'Passable', 
                                               'Assez Bien', 'Bien', 'Très Bien']) #Catégoriser les notes
        
        self.data = df
        print("✅ Données nettoyées avec succès")
        return self.data
    
    def get_summary(self):
        """Affiche un résumé des données"""
        if self.data is None:
            return None
        
        summary = {
            'Nombre_etudiants': self.data['ID_Etudiant'].nunique(),
            'Nombre_notes': len(self.data),
            'Departements': self.data['Departement'].nunique(),
            'Filières': self.data['Filière'].nunique(),
            'UEs': self.data['Nom_UE'].nunique(),
            'Matieres': self.data['Matiere'].nunique(),
            'Moyenne_finale': self.data['Note_Finale'].mean() if 'Note_Finale' in self.data.columns else None,
            'Taux_reussite': (self.data['Reussite'].mean() * 100) if 'Reussite' in self.data.columns else None
        }
        
        return summary