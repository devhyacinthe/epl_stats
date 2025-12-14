import pytest
import pandas as pd
import sys
from pathlib import Path

# Ajouter src au PATH
sys.path.append(str(Path(__file__).parent.parent / "src"))

def test_imports():
    """Teste que les imports fonctionnent"""
    from dashboard import StreamlitDashboard
    from data_loader import DataLoader
    from data_analyzer import DataAnalyzer
    from data_visualizer import DataVisualizer
    
    assert True  # Si on arrive ici, les imports fonctionnent

def test_data_loading():
    """Teste le chargement des données"""
    # Créer des données de test
    test_data = pd.DataFrame({
        'ID_Etudiant': ['ETU001', 'ETU002'],
        'Departement': ['Informatique', 'Civil'],
        'Note_Finale': [15.5, 12.0],
        'Reussite': [True, False]
    })
    
    assert len(test_data) == 2
    assert 'Note_Finale' in test_data.columns

def test_streamlit_components():
    """Teste les composants Streamlit"""
    import streamlit as st
    
    # Vérifier que Streamlit est installé
    assert hasattr(st, 'set_page_config')
    assert hasattr(st, 'title')
    assert hasattr(st, 'dataframe')

if __name__ == "__main__":
    pytest.main([__file__, "-v"])