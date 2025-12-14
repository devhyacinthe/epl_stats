import numpy as np

class DataAnalyzer:
    def __init__(self, dataframe):
        self.df = dataframe
    
    def calculate_basic_statistics(self):
        """Calcule les statistiques descriptives de base"""
        stats_dict = {}
        
        # Statistiques globales
        stats_dict['global'] = self._calculate_stats(self.df['Note_Finale'])
        
        # Par département
        stats_dict['par_departement'] = self._calculate_group_stats('Departement')
        
        # Par filière
        stats_dict['par_filiere'] = self._calculate_group_stats('Filière')
        
        # Par UE
        stats_dict['par_ue'] = self._calculate_group_stats('Nom_UE')
        
        # Par matière
        stats_dict['par_matiere'] = self._calculate_group_stats('Matiere')
        
        # Par enseignant
        stats_dict['par_enseignant'] = self._calculate_group_stats('Enseignant')
        
        return stats_dict
    
    def _calculate_stats(self, data_series):
        """Calcule les statistiques pour une série de données"""
        return {
            'moyenne': data_series.mean(),
            'mediane': data_series.median(),
            'ecart_type': data_series.std(),
            'variance': data_series.var(),
            'minimum': data_series.min(),
            'maximum': data_series.max(),
            'q1': data_series.quantile(0.25),
            'q3': data_series.quantile(0.75),
            'iqr': data_series.quantile(0.75) - data_series.quantile(0.25),
            'count': len(data_series),
            'skewness': data_series.skew(),
            'kurtosis': data_series.kurtosis()
        }
    
    def _calculate_group_stats(self, group_column):
        """Calcule les statistiques par groupe"""
        grouped = self.df.groupby(group_column)['Note_Finale'].apply(self._calculate_stats) #on applique la fonction de stats à chaque groupe
        return grouped.to_dict()
    
    def calculate_success_rate(self, groupby_column=None):
        """Calcule le taux de réussite"""
        if groupby_column:
            results = self.df.groupby(groupby_column).agg({
                'Reussite_Bool': ['mean', 'count'],
                'Note_Finale': 'mean'
            })
            results.columns = ['Taux_reussite', 'Nombre_notes', 'Moyenne_finale']
            results['Taux_reussite'] = results['Taux_reussite'] * 100
        else:
            results = {
                'Taux_reussite': self.df['Reussite_Bool'].mean() * 100,
                'Nombre_notes': len(self.df),
                'Moyenne_finale': self.df['Note_Finale'].mean()
            }
        
        return results
    
    def calculate_correlation(self):
        """Calcule les corrélations entre les notes"""
        correlation_matrix = self.df[['Note_Devoir', 'Note_Examen', 'Note_Finale']].corr()
        return correlation_matrix
    
    def get_student_ranking(self, top_n=50):
        """Classe les étudiants par moyenne générale"""
        student_avg = self.df.groupby('ID_Etudiant').agg({
            'Nom': 'first',
            'Prenom': 'first',
            'Departement': 'first',
            'Filière': 'first',
            'Note_Finale': ['mean', 'count'],
        }) #on groupe par étudiant
        
        student_avg.columns = ['Nom', 'Prenom', 'Departement', 'Filière', 
                              'Moyenne_Generale', 'Nombre_notes']
        
       
        student_avg = student_avg.sort_values('Moyenne_Generale', ascending=False)
        
        return student_avg.head(top_n)
    
    def analyze_distribution(self, groupby_column=None, group_value=None):
        """Analyse la distribution des notes"""
        if groupby_column and group_value:
            data = self.df[self.df[groupby_column] == group_value]['Note_Finale'] #Filtrer les données pour le groupe spécifié
        else:
            data = self.df['Note_Finale']
        
        # Créer des bins pour l'histogramme
        bins = np.arange(0, 21, 1) # Bins de 0 à 20 avec un pas de 1
        hist, bin_edges = np.histogram(data, bins=bins)
        
        distribution = {
            'bins': bin_edges[:-1], #on enlève le dernier bord de bin
            'frequence': hist,
            'frequence_relative': hist / len(data) * 100,
            'frequence_cumulative': np.cumsum(hist) / len(data) * 100
        }
        
        return distribution
    
    def compare_groups(self, group_column='Departement'):
        """Compare les performances entre groupes"""
        comparison = self.df.groupby(group_column).agg({
            'Note_Finale': ['mean', 'median', 'std', 'count', 'min', 'max', 'var'],
            'Reussite_Bool': 'mean',
            'Note_Devoir': 'mean',
            'Note_Examen': 'mean'
        }).round(2)
        
        comparison.columns = ['Moyenne_Finale', 'Mediane', 'Ecart_type', 'Count',
                              'Min', 'Max', 'Variance',
                            'Taux_reussite', 'Moyenne_Devoir', 'Moyenne_Examen']
        comparison['Taux_reussite'] = comparison['Taux_reussite'].apply(lambda x: np.ceil(float(x) * 100))
        
        
        return comparison