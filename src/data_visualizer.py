import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import os


class DataVisualizer:
    def __init__(self, dataframe):
        self.df = dataframe
        plt.style.use('seaborn-v0_8-darkgrid')
        self.colors = px.colors.qualitative.Set3
    
    def create_dashboard_visualizations(self, save_path=None):
        """Crée toutes les visualisations principales"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        
        # 1. Distribution des notes finales
        self._plot_distribution(axes[0, 0])
        
        # 2. Boxplot par département
        self._plot_boxplot_by(axes[0, 1], 'Departement')
        
        # 3. Taux de réussite par filière
        self._plot_success_rate(axes[0, 2], 'Filière')
        
        # 4. Corrélation entre devoir et examen
        self._plot_correlation(axes[1, 0])
        
        # 5. Évolution par année d'étude
        self._plot_by_year(axes[1, 1])
        
        # 6. Heatmap des moyennes par département/filière
        self._plot_heatmap(axes[1, 2])
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(f'{save_path}/dashboard_visualizations.png', 
                       dpi=300, bbox_inches='tight')
        
        return fig
    
    def _plot_distribution(self, ax):
        """Histogramme de la distribution"""
        ax.hist(self.df['Note_Finale'], bins=20, edgecolor='black', 
               alpha=0.7, color=self.colors[0])
        ax.axvline(10, color='red', linestyle='--', alpha=0.7, label='Seuil (10)')
        ax.set_xlabel('Note Finale /20')
        ax.set_ylabel('Fréquence')
        ax.set_title('Distribution des Notes Finales')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_boxplot_by(self, ax, column):
        """Boxplot par catégorie"""
        data_to_plot = []
        labels = []
        
        for group in sorted(self.df[column].unique()):
            data_to_plot.append(self.df[self.df[column] == group]['Note_Finale'])
            labels.append(group)
        
        ax.boxplot(data_to_plot, labels=labels)
        ax.axhline(10, color='red', linestyle='--', alpha=0.7)
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.set_ylabel('Note Finale /20')
        ax.set_title(f'Distribution par {column}')
        ax.grid(True, alpha=0.3)
    
    def _plot_success_rate(self, ax, column):
        """Tracé du taux de réussite par catégorie"""
        success_rate = self.df.groupby(column)['Reussite'].mean() * 100
        
        bars = ax.bar(range(len(success_rate)), success_rate.values, 
                    color=self.colors[:len(success_rate)])
        ax.set_xticks(range(len(success_rate)))
        ax.set_xticklabels(success_rate.index, rotation=45, ha='right')
        ax.set_ylabel('Taux de Réussite (%)')
        ax.set_title(f'Taux de Réussite par {column}')
        ax.axhline(50, color='red', linestyle='--', alpha=0.5, label='50%')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Ajouter les valeurs sur les barres
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.1f}%', ha='center', va='bottom', fontsize=9)
        
    def _plot_correlation(self, ax):
        """Tracé de corrélation entre devoir et examen"""
        ax.scatter(self.df['Note_Devoir'], self.df['Note_Examen'], 
                alpha=0.6, color=self.colors[3], edgecolors='black', linewidth=0.5)
        
        # Ligne de régression
        z = np.polyfit(self.df['Note_Devoir'], self.df['Note_Examen'], 1)
        p = np.poly1d(z)
        ax.plot(self.df['Note_Devoir'], p(self.df['Note_Devoir']), 
                color='red', linewidth=2, alpha=0.8)
        
        ax.set_xlabel('Note Devoir /20')
        ax.set_ylabel('Note Examen /20')
        ax.set_title('Corrélation Devoir vs Examen')
        ax.grid(True, alpha=0.3)
        
        # Ajouter le coefficient de corrélation
        correlation = self.df['Note_Devoir'].corr(self.df['Note_Examen'])
        ax.text(0.05, 0.95, f'r = {correlation:.3f}', 
                transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    

    def _plot_by_year(self, ax):
        """Tracé de l'évolution par année d'étude"""
        if 'Annee_etude' in self.df.columns:
            year_stats = self.df.groupby('Annee_etude').agg({
                'Note_Finale': ['mean', 'std', 'count'],
                'Reussite': 'mean'
            }).round(2)
            
            years = year_stats.index
            means = year_stats[('Note_Finale', 'mean')]
            errors = year_stats[('Note_Finale', 'std')]
            
            ax.errorbar(years, means, yerr=errors, fmt='o-', capsize=5, 
                    color=self.colors[4], linewidth=2, markersize=8)
            
            # Ajouter les taux de réussite
            ax2 = ax.twinx()
            success_rates = year_stats[('Reussite', 'mean')] * 100
            ax2.bar(years, success_rates, alpha=0.3, color=self.colors[5])
            ax2.set_ylabel('Taux de Réussite (%)', color=self.colors[5])
            ax2.tick_params(axis='y', labelcolor=self.colors[5])
            
            ax.set_xlabel('Année d\'Étude')
            ax.set_ylabel('Moyenne des Notes')
            ax.set_title('Évolution des Performances par Année')
            ax.grid(True, alpha=0.3)
            
            # Légende personnalisée
            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor=self.colors[4], alpha=0.5, label='Moyenne ± écart-type'),
                Patch(facecolor=self.colors[5], alpha=0.3, label='Taux de réussite')
            ]
            ax.legend(handles=legend_elements, loc='best')
        else:
            ax.text(0.5, 0.5, 'Données d\'année non disponibles', 
                    ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Évolution par Année (Données manquantes)')
    
    def _plot_heatmap(self, ax):
        """Heatmap des moyennes par département et filière"""
        if 'Departement' in self.df.columns and 'Filière' in self.df.columns:
            pivot_table = self.df.pivot_table(
                values='Note_Finale', 
                index='Departement', 
                columns='Filière', 
                aggfunc='mean'
            ).round(1)
            
            im = ax.imshow(pivot_table.values, cmap='YlOrRd', aspect='auto')
            
            # Labels
            ax.set_xticks(np.arange(len(pivot_table.columns)))
            ax.set_yticks(np.arange(len(pivot_table.index)))
            ax.set_xticklabels(pivot_table.columns, rotation=45, ha='right')
            ax.set_yticklabels(pivot_table.index)
            
            # Valeurs dans les cellules
            for i in range(len(pivot_table.index)):
                for j in range(len(pivot_table.columns)):
                    value = pivot_table.iloc[i, j]
                    if not pd.isna(value):
                        text_color = 'white' if value > 12 else 'black'
                        ax.text(j, i, f'{value:.1f}', 
                            ha='center', va='center', 
                            color=text_color, fontsize=9, fontweight='bold')
            
            ax.set_title('Moyennes par Département/Filière')
            plt.colorbar(im, ax=ax, label='Moyenne des notes')
        else:
            ax.text(0.5, 0.5, 'Données insuffisantes pour la heatmap', 
                    ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Heatmap (Données manquantes)')

    def create_interactive_dashboard(self):
        """Crée un dashboard interactif avec Plotly"""
        fig = make_subplots(
            rows=3, cols=3,
            subplot_titles=(
                'Distribution des Notes', 'Boxplot par Département',
                'Taux de Réussite', 'Corrélation Devoir/Examen',
                'Classement des Départements', 'Moyenne par Enseignant',
                'Évolution par Année', 'Heatmap des Performances',
                'Top 10 Matières'
            ),
            specs=[
                [{'type': 'xy'}, {'type': 'xy'}, {'type': 'xy'}],
                [{'type': 'xy'}, {'type': 'xy'}, {'type': 'xy'}],
                [{'type': 'xy'}, {'type': 'xy'}, {'type': 'xy'}]
            ],
            vertical_spacing=0.2,
            horizontal_spacing=0.2,
        )
        
        # Ajouter tous les graphiques
        self._add_histogram(fig, row=1, col=1)
        self._add_department_boxplot(fig, row=1, col=2)
        self._add_success_rate_bars(fig, row=1, col=3)
        self._add_correlation_scatter(fig, row=2, col=1)
        self._add_department_ranking(fig, row=2, col=2)
        self._add_teacher_performance(fig, row=2, col=3)
        self._add_year_evolution(fig, row=3, col=1)
        self._add_heatmap_interactive(fig, row=3, col=2)
        self._add_top_matiere(fig, row=3, col=3)
        
        fig.update_layout(
            height=1400,
           
            title_text="Dashboard Interactif - Analyse des Notes EPL",
            title_font_size=20,
            hovermode='closest'
        )
        
        return fig
    
    def create_advanced_visualizations(self):
        """Crée des visualisations avancées supplémentaires"""
        visualizations = {}
        
        # 1. Matrice de corrélation
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        correlation_matrix = self.df[numeric_cols].corr()
        
        fig_corr = px.imshow(correlation_matrix, text_auto='.2f',
                            color_continuous_scale='RdBu_r',
                            title='Matrice de Corrélation')
                
        visualizations['correlation_matrix'] = fig_corr
        
        # 2. Violin plot par département
        fig_violin = px.violin(self.df, x='Departement', y='Note_Finale',
                            box=True, points='all',
                            title='Distribution Violin par Département')
        visualizations['violin_departements'] = fig_violin
        
        # 3. Scatter matrix
        if len(numeric_cols) >= 3:
            fig_scatter_matrix = px.scatter_matrix(self.df[numeric_cols].iloc[:, :4],
                                                title='Scatter Matrix des Variables Numériques')
            visualizations['scatter_matrix'] = fig_scatter_matrix
        
        # 4. Graphique à bulles (année vs moyenne vs effectif)
        if 'Annee_etude' in self.df.columns:
            year_summary = self.df.groupby('Annee_etude').agg({
                'Note_Finale': 'mean',
                'ID_Etudiant': 'nunique',
                'Reussite': 'mean'
            }).reset_index()
            
            fig_bubble = px.scatter(year_summary, 
                                x='Annee_etude',
                                y='Note_Finale',
                                size='ID_Etudiant',
                                color='Reussite',
                                size_max=60,
                                hover_name='Annee_etude',
                                title='Performance par Année (taille = nombre étudiants)')
            visualizations['bubble_year'] = fig_bubble
        
        return visualizations

    def export_advanced_visualizations(self, output_dir='outputs/visualizations/advanced'):
        """Exporte les visualisations avancées"""
        os.makedirs(output_dir, exist_ok=True)
        
        advanced_viz = self.create_advanced_visualizations()
        
        for name, fig in advanced_viz.items():
            fig.write_html(f"{output_dir}/{name}.html")
            fig.write_image(f"{output_dir}/{name}.png", width=1200, height=800)
        
        print(f"✅ Visualisations avancées exportées dans {output_dir}/")
        
        return advanced_viz
    
    def _add_histogram(self, fig, row, col):
        """Ajoute un histogramme interactif"""
        fig.add_trace(
            go.Histogram(
                x=self.df['Note_Finale'],
                nbinsx=20,
                name='Distribution',
                marker_color=self.colors[0]
            ),
            row=row, col=col
        )
    
    def _add_department_boxplot(self, fig, row, col):
        """Ajoute un boxplot par département"""
        for dept in self.df['Departement'].unique():
            data_dept = self.df[self.df['Departement'] == dept]['Note_Finale']
            fig.add_trace(
                go.Box(
                    y=data_dept,
                    name=dept,
                    boxpoints='outliers'
                ),
                row=row, col=col
            )
    
    def _add_success_rate_bars(self, fig, row, col):
        success_rate = self.df.groupby('Filière')['Reussite'].mean() * 100
        fig.add_trace(
            go.Bar(
                x=success_rate.index,
                y=success_rate.values,
                name='Taux réussite',
                marker_color='#2ca02c',
                showlegend=False
            ),
            row=row, col=col
        )
    
    def _add_correlation_scatter(self, fig, row, col):
        fig.add_trace(
            go.Scatter(
                x=self.df['Note_Examen'],
                y=self.df['Note_Devoir'],
                mode='markers',
                name='Corrélation',
                marker=dict(color=self.colors[1], size=6, opacity=0.6),
                showlegend=False
            ),
            row=row, col=col
        )
        fig.update_xaxes(title_text='Note Examen', row=row, col=col)
        fig.update_yaxes(title_text='Note Devoir', row=row, col=col)
    
    def _add_department_ranking(self, fig, row, col):
        dept_avg = self.df.groupby('Departement')['Note_Finale'].mean().sort_values(ascending=False)
        fig.add_trace(
            go.Bar(
                x=dept_avg.index,
                y=dept_avg.values,
                name='Classement Départements',
                marker_color=self.colors[2],
                showlegend=False
            ),
            row=row, col=col
        )
        fig.update_xaxes(title_text='Département', row=row, col=col)
        fig.update_yaxes(title_text='Moyenne Note Finale', row=row, col=col)

    def _add_teacher_performance(self, fig, row, col):
        teacher_avg = self.df.groupby('Enseignant')['Note_Finale'].mean().sort_values(ascending=False)
        fig.add_trace(
            go.Bar(
                x=teacher_avg.index,
                y=teacher_avg.values,
                name='Performance Enseignants',
                marker_color=self.colors[3],
                showlegend=False
            ),
            row=row, col=col
        )
        fig.update_xaxes(title_text='Enseignant', row=row, col=col)
        fig.update_yaxes(title_text='Moyenne Note Finale', row=row, col=col)

    def _add_heatmap_interactive(self, fig, row, col):
        """Ajoute une heatmap interactive"""
        if 'Departement' in self.df.columns and 'Filière' in self.df.columns:
            pivot_table = self.df.pivot_table(
                values='Note_Finale', 
                index='Departement', 
                columns='Filière', 
                aggfunc='mean'
            ).round(1)
            
            fig.add_trace(
                go.Heatmap(
                    z=pivot_table.values,
                    x=pivot_table.columns,
                    y=pivot_table.index,
                    colorscale='YlOrRd',
                    colorbar=dict(title='Moyenne'),
                    hovertemplate='Département: %{y}<br>Filière: %{x}<br>Moyenne: %{z:.1f}<extra></extra>'
                ),
                row=row, col=col
            )
        else:
            fig.add_annotation(
                x=0.5, y=0.5,
                text="Données insuffisantes",
                showarrow=False,
                row=row, col=col
            )

    def _add_year_evolution(self, fig, row, col):
        """Ajoute le graphique d'évolution par année"""
        if 'Annee_etude' in self.df.columns:
            year_stats = self.df.groupby('Annee_etude').agg({
                'Note_Finale': ['mean', 'std'],
                'Reussite': 'mean'
            }).round(2)
            
            years = year_stats.index
            means = year_stats[('Note_Finale', 'mean')]
            errors = year_stats[('Note_Finale', 'std')]
            
            # Graphique des moyennes
            fig.add_trace(
                go.Scatter(
                    x=years,
                    y=means,
                    mode='lines+markers',
                    name='Moyenne',
                    line=dict(color=self.colors[4], width=3),
                    error_y=dict(
                        type='data',
                        array=errors,
                        visible=True,
                        color='gray'
                    )
                ),
                row=row, col=col
            )
            
            # Graphique des taux de réussite (sur le même subplot)
            success_rates = year_stats[('Reussite', 'mean')] * 100
            fig.add_trace(
                go.Bar(
                    x=years,
                    y=success_rates,
                    name='Taux réussite',
                    marker_color=self.colors[5],
                    opacity=0.5,
                    yaxis='y2'
                ),
                row=row, col=col
            )
            
            # Configuration des axes doubles
            fig.update_layout({
                f'yaxis2': dict(
                    title='Taux réussite (%)',
                    overlaying='y',
                    side='right',
                    range=[0, 100]
                )
            })
            
            fig.update_xaxes(title_text='Année', row=row, col=col)
            fig.update_yaxes(title_text='Moyenne notes', row=row, col=col)
        else:
            fig.add_annotation(
                x=0.5, y=0.5,
                text="Données d'année non disponibles",
                showarrow=False,
                row=row, col=col
            )

    def _add_top_matiere(self, fig, row, col):
        """Ajoute le top 10 des matières"""
        if 'Matiere' in self.df.columns:
            matiere_stats = self.df.groupby('Matiere').agg({
                'Note_Finale': ['mean', 'count'],
                'Reussite': 'mean'
            }).round(2)
            
            # Filtrer les matières avec au moins 10 notes
            matiere_stats = matiere_stats[matiere_stats[('Note_Finale', 'count')] >= 10]
            
            # Trier par moyenne et prendre les top 10
            top_10 = matiere_stats.nlargest(10, ('Note_Finale', 'mean'))
            
            fig.add_trace(
                go.Bar(
                    x=top_10[('Note_Finale', 'mean')],
                    y=top_10.index,
                    orientation='h',
                    marker_color=self.colors[6],
                    hovertemplate='Matière: %{y}<br>Moyenne: %{x:.2f}<br>Étudiants: %{customdata}<extra></extra>',
                    customdata=top_10[('Note_Finale', 'count')].values
                ),
                row=row, col=col
            )
            
            fig.update_xaxes(title_text='Moyenne', row=row, col=col)
            fig.update_yaxes(title_text='Matière', row=row, col=col)
        else:
            fig.add_annotation(
                x=0.5, y=0.5,
                text="Données de matière non disponibles",
                showarrow=False,
                row=row, col=col
            )
    
    def export_visualizations(self, output_dir='outputs/visualizations'):
        """Exporte toutes les visualisations"""
        
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Dashboard complet
        dashboard_fig = self.create_interactive_dashboard()
        dashboard_fig.write_html(f"{output_dir}/dashboard_interactif.html")
        
        # Pour l'export PNG, on peut avoir besoin de kaleido
        try:
            dashboard_fig.write_image(f"{output_dir}/dashboard_interactif.png", width=1200, height=1400)
        except Exception as e:
            print(f"⚠️ Impossible d'exporter en PNG (kaleido peut être requis): {e}")
        
        # 2. Graphiques individuels
        self._export_individual_plots(output_dir)
        
        # 3. Visualisations avancées
        self.export_advanced_visualizations(f"{output_dir}/advanced")
        
        print(f"✅ Visualisations exportées dans {output_dir}/")
        
        return True

    def _export_individual_plots(self, output_dir):
        """Exporte les graphiques individuels"""
        
        # Distribution
        fig1 = px.histogram(self.df, x='Note_Finale', nbins=20,
                           title='Distribution des Notes Finales')
        fig1.write_html(f'{output_dir}/distribution.html')
        
        # Boxplot par département
        fig2 = px.box(self.df, x='Departement', y='Note_Finale',
                     title='Distribution par Département')
        fig2.write_html(f'{output_dir}/boxplot_departements.html')
        
        # Taux de réussite par filière
        if 'Filière' in self.df.columns:
            success_rate = self.df.groupby('Filière')['Reussite'].mean() * 100
            fig3 = px.bar(x=success_rate.index, y=success_rate.values,
                         title='Taux de Réussite par Filière',
                         labels={'x': 'Filière', 'y': 'Taux de Réussite (%)'})
            fig3.write_html(f'{output_dir}/taux_reussite_filiere.html')
        
        # Corrélation
        if 'Note_Devoir' in self.df.columns and 'Note_Examen' in self.df.columns:
            fig4 = px.scatter(self.df, x='Note_Devoir', y='Note_Examen',
                             trendline='ols',
                             title='Corrélation Devoir vs Examen',
                             labels={'Note_Devoir': 'Note Devoir', 'Note_Examen': 'Note Examen'})
            fig4.write_html(f'{output_dir}/correlation.html')
        
        # Évolution par année
        if 'Annee_etude' in self.df.columns:
            year_stats = self.df.groupby('Annee_etude').agg({
                'Note_Finale': 'mean',
                'Reussite': 'mean'
            }).reset_index()
            
            fig5 = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Moyennes
            fig5.add_trace(
                go.Scatter(x=year_stats['Annee_etude'], y=year_stats['Note_Finale'],
                          mode='lines+markers', name='Moyenne notes',
                          line=dict(color='blue', width=3)),
                secondary_y=False
            )
            
            # Taux de réussite
            fig5.add_trace(
                go.Bar(x=year_stats['Annee_etude'], y=year_stats['Reussite']*100,
                      name='Taux réussite', opacity=0.5,
                      marker_color='orange'),
                secondary_y=True
            )
            
            fig5.update_layout(title_text='Évolution par Année d\'Étude')
            fig5.update_xaxes(title_text="Année d'étude")
            fig5.update_yaxes(title_text="Moyenne notes", secondary_y=False)
            fig5.update_yaxes(title_text="Taux réussite (%)", secondary_y=True)
            
            fig5.write_html(f'{output_dir}/evolution_annee.html')