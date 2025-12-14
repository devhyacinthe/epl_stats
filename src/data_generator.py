import pandas as pd
import numpy as np
from datetime import datetime
import random
import sys
import os
from faker import Faker

sys.stdout.reconfigure(encoding='utf-8') # Pour afficher les caractères spéciaux correctement


class DataGenerator:
    def __init__(self, n_etudiants=1200, seed=42):
        self.n_etudiants = n_etudiants
        np.random.seed(seed)
        random.seed(seed) # Pour toujours avoir les mêmes données
        self.fake = Faker('fr_FR') # 'fr_FR' pour le français
        
        
        # Départements EPL avec probabilités de distribution
        self.departements = [
            'Génie Informatique', 'Génie Civil', 'Génie Mécanique', 'Génie Électrique'
        ]
        

        # Distribution aléatoire basée sur la popularité des départements
        self.departement_distribution = {
            'Génie Informatique': 0.35,  
            'Génie Civil': 0.25,         
            'Génie Mécanique': 0.20,      
            'Génie Électrique': 0.20      
        }
        

        # Vérification que la somme des probabilités est 1
        total_prob = sum(self.departement_distribution.values())
        if abs(total_prob - 1.0) > 0.001:
            raise ValueError(f"La somme des probabilités doit être égale à 1. Somme actuelle: {total_prob}")
        

        # Structures par département avec codes d'UE et matières
        self.structure = {
            'Génie Informatique': {
                'grades': ['Licence professionnelle', 'Master Professionnel'],
                'filière': ['Génie Logiciel', 'Système et réseaux', 'IA et Big Data', 'Système Informatique', 'Logistique'],
                'ue': {
                    'Génie Logiciel': {
                        'INF2101': ['Algorithmique Avancée', 'Structures de données avancées', 'Analyse d\'algorithmes', 'Graphes et optimisation'],
                        'INF2102': ['Développement Logiciel', 'Design Patterns', 'Architecture logicielle', 'Tests unitaires et TDD'],
                        'INF2103': ['Ingénierie des SI', 'UML et modélisation', 'Cycle de vie des projets', 'Gestion des exigences']
                    },
                    'Système et réseaux': {
                        'INF2201': ['Réseaux et Communications', 'TCP/IP avancé', 'Routage et commutation', 'Réseaux sans fil'],
                        'INF2202': ['Sécurité Informatique', 'Cryptographie appliquée', 'Pare-feu et IDS/IPS', 'Audit de sécurité'],
                        'INF2203': ['Administration Système', 'Linux serveur', 'Scripting shell', 'Virtualisation et conteneurs']
                    },
                    'Système Informatique': {
                        'INF2301': ['Architecture Matérielle', 'Microprocesseurs', 'Systèmes embarqués', 'Architecture parallèle'],
                        'INF2302': ['Systèmes d\'Exploitation', 'Noyau et drivers', 'Gestion de la mémoire', 'Ordonnancement'],
                        'INF2303': ['Robotique et Automatisme', 'Capteurs et actionneurs', 'Asservissements', 'Vision par ordinateur']
                    },
                    'IA et Big Data': {
                        'INF2401': ['Intelligence Artificielle', 'Apprentissage automatique', 'Réseaux de neurones', 'Traitement du langage naturel'],
                        'INF2402': ['Data Science', 'Statistiques avancées', 'Visualisation de données', 'Data Mining'],
                        'INF2403': ['Big Data Technologies', 'Hadoop et Spark', 'Bases NoSQL', 'Traitement en streaming']
                    },
                    'Logistique': {
                        'INF2501': ['Supply Chain Management', 'Gestion des stocks', 'Planification logistique', 'Transport et distribution'],
                        'INF2502': ['Systèmes d\'Information Logistique', 'ERP logistique', 'Traçabilité RFID', 'Optimisation des flux'],
                        'INF2503': ['E-logistique', 'E-commerce et logistique', 'Plateformes digitales', 'Last mile delivery']
                    }
                }
            },
            
            'Génie Électrique': {
                'grades': ['Licence Fondamentale', 'Master', 'Doctorat'],
                'filière': ['Électrotechnique', 'Automatique et Contrôle', 'Énergies Renouvelables', 'Électronique de Puissance', 'Réseaux Intelligents'],
                'ue': {
                    'Électrotechnique': {
                        'ELE2101': ['Machines Électriques', 'Machines à courant continu', 'Machines synchrones', 'Machines asynchrones'],
                        'ELE2102': ['Conversion d\'Énergie', 'Redresseurs et onduleurs', 'Convertisseurs DC-DC', 'Alimentations à découpage'],
                        'ELE2103': ['Diagnostic des Systèmes', 'Analyse vibratoire', 'Thermographie infrarouge', 'Analyse des courants']
                    },
                    'Automatique et Contrôle': {
                        'ELE2201': ['Automatismes Industriels', 'GRAFCET et SFC', 'API Programmable', 'Bus de terrain'],
                        'ELE2202': ['Régulation Avancée', 'PID adaptatif', 'Commande prédictive', 'Observation d\'état'],
                        'ELE2203': ['Systèmes Embarqués', 'Microcontrôleurs', 'Traitement du signal', 'Temps réel dur']
                    },
                    'Énergies Renouvelables': {
                        'ELE2301': ['Solaire Photovoltaïque', 'Cellules PV', 'Onduleurs solaires', 'Dimensionnement de centrales'],
                        'ELE2302': ['Éolien', 'Aérogénérateurs', 'Conversion éolienne', 'Intégration au réseau'],
                        'ELE2303': ['Stockage d\'Énergie', 'Batteries Li-ion', 'Supercondensateurs', 'Power-to-Gas']
                    },
                    'Électronique de Puissance': {
                        'ELE2401': ['Convertisseurs Statiques', 'Hacheurs série/parallèle', 'Onduleurs MLI', 'Gradateurs'],
                        'ELE2402': ['Compatibilité Électromagnétique', 'Perturbations conduites', 'Rayonnements', 'Blindage et filtrage'],
                        'ELE2403': ['Thermique des Composants', 'Dissipation thermique', 'Refroidissement actif', 'Matériaux thermiques']
                    },
                    'Réseaux Intelligents': {
                        'ELE2501': ['Smart Grids', 'Compteurs intelligents', 'Gestion de la demande', 'Micro-réseaux'],
                        'ELE2502': ['Protection des Réseaux', 'Relais numériques', 'Coordination des protections', 'Stabilité dynamique'],
                        'ELE2503': ['Qualité de l\'Énergie', 'Harmoniques', 'Fluctuations de tension', 'Correcteurs actifs']
                    }
                }
            },
            
            'Génie Mécanique': {
                'grades': ['Licence Fondamentale',  'Master', 'Doctorat'],
                'filière': ['Conception Mécanique', 'Énergétique et Thermodynamique', 'Production Industrielle', 'Matériaux et Procédés', 'Robotique Avancée'],
                'ue': {
                    'Conception Mécanique': {
                        'MEC2101': ['CAO/DAO Avancé', 'Modélisation paramétrique', 'Assemblages complexes', 'Gestion des contraintes'],
                        'MEC2102': ['Calcul des Structures', 'Éléments finis avancés', 'Fatigue des matériaux', 'Dynamique des structures'],
                        'MEC2103': ['Tolérancement', 'Chaînes de cotes', 'Statistiques de fabrication', 'Métrologie 3D']
                    },
                    'Énergétique et Thermodynamique': {
                        'MEC2201': ['Machines Thermiques', 'Turbines à gaz', 'Moteurs Diesel', 'Cycle de Rankine'],
                        'MEC2202': ['Transferts Thermiques', 'Convection forcée/naturelle', 'Rayonnement thermique', 'Échangeurs de chaleur'],
                        'MEC2203': ['Énergies Nouvelles', 'Piles à combustible', 'Cogénération', 'Valorisation énergétique']
                    },
                    'Production Industrielle': {
                        'MEC2301': ['Usinage CNC', 'Programmation ISO', 'Simulation d\'usinage', 'Optimisation de trajectoires'],
                        'MEC2302': ['Fabrication Additive', 'Impression 3D métal', 'SLA et SLS', 'Contrôle qualité AM'],
                        'MEC2303': ['Métrologie Industrielle', 'Machines à mesurer', 'Rugosimètres', 'Projecteurs de profils']
                    },
                    'Matériaux et Procédés': {
                        'MEC2401': ['Science des Matériaux', 'Diagrammes de phases', 'Transformations structurales', 'Propriétés mécaniques'],
                        'MEC2402': ['Procédés de Fabrication', 'Injection plastique', 'Emboutissage', 'Frittage'],
                        'MEC2403': ['Traitements de Surface', 'Traitements thermiques', 'Revêtements PVD/CVD', 'Nitruration']
                    },
                    'Robotique Avancée': {
                        'MEC2501': ['Cinématique et Dynamique', 'Modèles géométriques', 'Jacobien', 'Dynamique inverse'],
                        'MEC2502': ['Commande Robotique', 'Asservissement numérique', 'Planification de trajectoires', 'Force control'],
                        'MEC2503': ['Vision Industrielle', 'Traitement d\'images', 'Reconnaissance de formes', 'Guidage visuel']
                    }
                }
            },
            
            'Génie Civil': {
                'grades': ['Licence Fondamentale',  'Master', 'Doctorat'],
                'filière': ['Bâtiment et Travaux Publics', 'Génie Structural', 'Géotechnique', 'Hydraulique et Environnement', 'Urbanisme et Transport'],
                'ue': {
                    'Bâtiment et Travaux Publics': {
                        'CIV2101': ['Technologie du Bâtiment', 'Gros œuvre', 'Second œuvre', 'Étanchéité toiture'],
                        'CIV2102': ['Matériaux de Construction', 'Béton haute performance', 'Bois lamellé-collé', 'Matériaux composites'],
                        'CIV2103': ['Sécurité Chantier', 'Étude de sécurité', 'Plans de prévention', 'Coordination SPS']
                    },
                    'Génie Structural': {
                        'CIV2201': ['Béton Armé et Précontraint', 'Calcul des sections', 'Dispositions constructives', 'Vérification ELU/ELS'],
                        'CIV2202': ['Construction Métallique', 'Assemblages soudés/boulonnés', 'Stabilité des structures', 'Eurocodes'],
                        'CIV2203': ['Dynamique des Structures', 'Analyse modale', 'Sismique', 'Vibrations induites']
                    },
                    'Géotechnique': {
                        'CIV2301': ['Mécanique des Sols', 'Contraintes efficaces', 'Tassements', 'Rupture des sols'],
                        'CIV2302': ['Fondations Spéciales', 'Pieux forés', 'Parois moulées', 'Inclusions rigides'],
                        'CIV2303': ['Ouvrages Souterrains', 'Tunnels', 'Galeries', 'Soutènements']
                    },
                    'Hydraulique et Environnement': {
                        'CIV2401': ['Hydrologie', 'Bilans hydriques', 'Crues décennales', 'Modélisation pluie-débit'],
                        'CIV2402': ['Traitement des Eaux', 'Potabilisation', 'Épuration des eaux usées', 'Déphosphatation'],
                        'CIV2403': ['Génie de l\'Environnement', 'Études d\'impact', 'Gestion des déchets', 'Dépollution des sols']
                    },
                    'Urbanisme et Transport': {
                        'CIV2501': ['Aménagement du Territoire', 'Plans locaux d\'urbanisme', 'Zones d\'aménagement concerté', 'Écoquartiers'],
                        'CIV2502': ['Infrastructures Routières', 'Géométrie des routes', 'Couches de chaussée', 'Signalisation'],
                        'CIV2503': ['Ouvrages d\'Art', 'Ponts en arc', 'Ponts à haubans', 'Viaducs']
                    }
                }
            },   
        }


        # Mapper les codes d'UE aux noms d'UE complets
        self.ue_code_to_name = {}
        for dept, dept_data in self.structure.items():
            for filiere, ue_dict in dept_data['ue'].items():
                for ue_code, ue_content in ue_dict.items():
                    self.ue_code_to_name[ue_code] = ue_content[0]  # Premier élément est le nom de l'UE
        
        # Enseignants fictifs
        self.enseignants = [self.fake.name() for _ in range(30)]
        
        # Coefficients pour calcul de la note finale
        self.coefficient_examen = 0.6  # Examen final compte pour 60%
        self.coefficient_devoir = 0.4  # Devoir compte pour 40%
        
        # Dictionnaire pour stocker les codes de matière par UE
        self.matiere_codes = {}
        
        # Variables pour le suivi de la distribution
        self.distribution_count = {dept: 0 for dept in self.departements}
    
    def select_departement(self, student_id, method='mixed'):
        """
        Sélectionne un département pour un étudiant selon plusieurs méthodes possibles
        
        Méthodes disponibles:
        1. 'fixed' : Distribution fixe avec probabilités prédéfinies
        2. 'random' : Distribution uniforme complètement aléatoire
        3. 'seasonal' : Variation selon la 'saison ou vague d'inscription' (position de l'étudiant)
        4. 'mixed' : Combinaison des méthodes
        """
    
        
        if method == 'fixed':
            # Méthode 1: Distribution fixe avec probabilités prédéfinies
            departements = list(self.departement_distribution.keys())
            probabilities = list(self.departement_distribution.values())
            dept = np.random.choice(departements, p=probabilities)
            
        elif method == 'random':
            # Méthode 2: Distribution uniforme complètement aléatoire
            dept = np.random.choice(self.departements)
            
        elif method == 'seasonal':
            # Méthode 3: Variation saisonnière (les premiers étudiants ont une distribution différente)
            season_factor = student_id / self.n_etudiants # Ici, on utilise ID de l'etudiant et cette ID est unique et croissante(nombre entier) donc, plus l'ID est élevé, plus on avance dans la 'saison'
            
            if season_factor < 0.33:  # Première 'saison' : plus d'étudiants en Informatique
                adjusted_probs = {
                    'Génie Informatique': 0.45,
                    'Génie Civil': 0.25,
                    'Génie Mécanique': 0.15,
                    'Génie Électrique': 0.15
                }
            elif season_factor < 0.66:  # Deuxième 'saison' : distribution équilibrée
                adjusted_probs = {
                    'Génie Informatique': 0.25,
                    'Génie Civil': 0.25,
                    'Génie Mécanique': 0.25,
                    'Génie Électrique': 0.25
                }
            else:  # Troisième 'saison' : plus d'étudiants en Civil/Mécanique
                adjusted_probs = {
                    'Génie Informatique': 0.20,
                    'Génie Civil': 0.35,
                    'Génie Mécanique': 0.25,
                    'Génie Électrique': 0.20
                }
            
            # Normaliser les probabilités
            total = sum(adjusted_probs.values())
            normalized_probs = {k: v/total for k, v in adjusted_probs.items()}
            
            departements = list(normalized_probs.keys())
            probabilities = list(normalized_probs.values())
            dept = np.random.choice(departements, p=probabilities)
            
        elif method == 'mixed':
            # Méthode 4: Combinaison avec légère variation aléatoire
            base_probs = self.departement_distribution.copy()
            
            # Ajouter un peu de bruit aléatoire (±5%)
            noise = np.random.normal(0, 0.05, len(base_probs))
            noisy_probs = {}
            
            for i, (dept_name, base_prob) in enumerate(base_probs.items()):
                noisy_prob = max(0.05, min(0.6, base_prob + noise[i]))  # Limiter entre 5% et 60%
                noisy_probs[dept_name] = noisy_prob
            
            # Normaliser pour que la somme soit 1
            total = sum(noisy_probs.values())
            normalized_probs = {k: v/total for k, v in noisy_probs.items()}
            
            departements = list(normalized_probs.keys())
            probabilities = list(normalized_probs.values())
            dept = np.random.choice(departements, p=probabilities)
            
        elif method == 'progressive':
            # Méthode 5: Ajustement progressif basé sur le nombre d'étudiants déjà attribués
            

            # Calculer les déviations
            deviations = {}
            for dept in self.departements:
                current_ratio = self.distribution_count[dept] / max(1, student_id)
                target_ratio = self.departement_distribution[dept]
                deviations[dept] = target_ratio - current_ratio
            
            # Convertir les déviations en probabilités
            # On utilise softmax pour convertir en probabilités
            deviation_values = np.array(list(deviations.values()))
            exp_values = np.exp(deviation_values * 5)  # Facteur d'échelle pour amplifier les différences
            probabilities = exp_values / exp_values.sum()
            
            dept = np.random.choice(self.departements, p=probabilities)
            
        else:
            # Méthode par défaut
            dept = np.random.choice(self.departements)
        
        # Mettre à jour le compteur
        self.distribution_count[dept] += 1
        
        return dept
    
    def generate_etudiant(self, id_etudiant, method):
        """Génère un étudiant avec son département selon une distribution aléatoire"""
        dept = self.select_departement(id_etudiant, method)
        grade = np.random.choice(self.structure[dept]['grades'])
        
        # Déterminer l'année d'étude basée sur le grade
        annee_mapping = {
            'Licence Fondamentale': np.random.choice([1, 2, 3], p=[0.4, 0.35, 0.25]),
            'Licence professionnelle': np.random.choice([1, 2, 3], p=[0.4, 0.35, 0.25]),
            'Master Professionnel': np.random.choice([1, 2], p=[0.6, 0.4]),
            'Master': np.random.choice([1, 2], p=[0.6, 0.4]),
            'Doctorat': np.random.choice([1, 2, 3], p=[0.5, 0.3, 0.2])
        }
        
        return {
            'ID_Etudiant': f'ETU{id_etudiant:04d}',
            'Nom': self.fake.last_name(),
            'Prenom': self.fake.first_name(),
            'Departement': dept,
            'Grade': grade,
            'Annee_etude': annee_mapping.get(grade, 1),
            'Niveau_Individuel': np.random.normal(0, 5)  # Capacité individuelle
        }
    
    def get_matiere_code(self, ue_code, matiere_index):
        """Génère un code de matière basé sur le code UE et l'index"""
        # Formater le code de matière: [premier chiffre] + code UE
        # Exemple: pour UE MTH2121, les matières seraient 1MTH2121, 2MTH2121, etc.
        return f"{matiere_index}{ue_code}"
    
    def generate_note_matiere(self, etudiant_info):
        """Génère les notes pour une matière spécifique"""
        dept = etudiant_info['Departement']
        annee_etude = etudiant_info['Annee_etude']
        niveau_indiv = etudiant_info['Niveau_Individuel']
        
        # Base de la note selon l'année et le niveau individuel
        base_note = 10 - annee_etude * 0.25 + niveau_indiv # Ici on ajuste la note de base selon l'année d'étude et le niveau individuel(plus ton année d'etude est élevée, plus la note de base diminue légèrement)
        
        # Ajustement selon la difficulté du département
        difficulte_departement = {
            'Génie Informatique': -1,
            'Génie Civil': -0.5,
            'Génie Mécanique': -0.5,
            'Génie Électrique': -1
        }
        base_note += difficulte_departement.get(dept, 0)
        
        # Générer note de devoir (plus variable)
        note_devoir = base_note + np.random.normal(1, 2.5) #Distribtution normale avec moyenne 1 et écart-type 2.5
        note_devoir = max(0, min(20, note_devoir))
        
        # Générer note d'examen (plus standardisée)
        note_examen = base_note + np.random.normal(1, 3.25)
        note_examen = max(0, min(20, note_examen)) #Limiter entre 0 et 20
        
        # Arrondir les notes
        note_devoir = round(note_devoir, 1)
        note_examen = round(note_examen, 1)

        # Calculer la note finale pondérée
        note_finale = (note_devoir * self.coefficient_devoir + 
                      note_examen * self.coefficient_examen)
        note_finale = round(max(0, min(20, note_finale)), 1)
        
        
        # Déterminer si l'étudiant a réussi
        reussite = note_finale >= 10
        
        return {
            'Note_Devoir': note_devoir,
            'Note_Examen': note_examen,
            'Note_Finale': note_finale,
            'Reussite': reussite
        }
    
    def generate_notes_etudiant(self, etudiant_info, nb_ues=5):
        """Génère toutes les notes pour un étudiant"""
        dept = etudiant_info['Departement']
        filiere = np.random.choice(self.structure[dept]['filière'])
        notes_data = []
        
        # Sélectionner aléatoirement des UE pour cet étudiant
        ue_dict = self.structure[dept]['ue'][filiere]
        ues_disponibles = list(ue_dict.keys())
        ues_selectionnees = np.random.choice(ues_disponibles, 
                                           size=min(nb_ues, len(ues_disponibles)), 
                                           replace=False)
        
        for ue_code in ues_selectionnees:
            ue_nom_complet = self.ue_code_to_name[ue_code]
            
            # Pour chaque UE, sélectionner 2-3 matières (en excluant le nom de l'UE lui-même)
            matieres_ue = ue_dict[ue_code][1:]  # Exclure le premier élément (nom de l'UE) (car je considère que le nom de l'UE n'est pas une matière)
            nb_matieres = np.random.randint(2, min(4, len(matieres_ue) + 1))
            matieres_selectionnees = np.random.choice(matieres_ue, 
                                                    size=nb_matieres, 
                                                    replace=False) #Le replace=False pour éviter la répétition des matières
            
            for i, matiere in enumerate(matieres_selectionnees, 1):
                # Générer les notes pour chaque matière
                notes_matiere = self.generate_note_matiere(etudiant_info)
                
                # Générer le code de la matière
                code_matiere = self.get_matiere_code(ue_code, matiere_index=i)
                
                # Créer l'entrée de données
                note_data = {
                    'ID_Etudiant': etudiant_info['ID_Etudiant'],
                    'Nom': etudiant_info['Nom'],
                    'Prenom': etudiant_info['Prenom'],
                    'Departement': dept,
                    'Grade': etudiant_info['Grade'],
                    'Annee_etude': etudiant_info['Annee_etude'],
                    'Filière': filiere,
                    'Code_UE': ue_code,
                    'Nom_UE': ue_nom_complet,
                    'Code_Matiere': code_matiere,
                    'Matiere': matiere,
                    'Enseignant': np.random.choice(self.enseignants),
                    'Note_Devoir': notes_matiere['Note_Devoir'],
                    'Note_Examen': notes_matiere['Note_Examen'],
                    'Note_Finale': notes_matiere['Note_Finale'],
                    'Reussite': notes_matiere['Reussite'],
                    'Date_Devoir': self.fake.date_between(start_date='-6M', end_date='-1M').strftime('%Y-%m-%d'),
                    'Date_Examen': self.fake.date_between(start_date='-1M', end_date='today').strftime('%Y-%m-%d'),
                    'Session': np.random.choice(['Principale', 'Rattrapage'], p=[0.85, 0.15]),
                    'Coefficient_Devoir': self.coefficient_devoir,
                    'Coefficient_Examen': self.coefficient_examen
                }
                notes_data.append(note_data)
        
        return notes_data
    
    def generate_dataset(self, method):
        """Génère le dataset complet"""
        data = []
        
        print(f"Génération de {self.n_etudiants} étudiants...")
        print("Chaque étudiant aura 5 UE avec 2-3 matières par UE")
        
        # Réinitialiser le compteur de distribution
        self.distribution_count = {dept: 0 for dept in self.departements}
        
        for i in range(1, self.n_etudiants + 1):
            etudiant = self.generate_etudiant(i, method)
            notes_etudiant = self.generate_notes_etudiant(etudiant, nb_ues=5)
            data.extend(notes_etudiant)
            
            # Afficher la progression
            if i % 100 == 0:
                print(f"  {i} étudiants générés...")
        
        df = pd.DataFrame(data) # Convertir en DataFrame
        
        # Réorganiser les colonnes pour une meilleure lisibilité
        colonnes = ['ID_Etudiant', 'Nom', 'Prenom', 'Departement', 'Grade', 'Annee_etude', 
                   'Filière', 'Code_UE', 'Nom_UE', 'Code_Matiere', 'Matiere', 'Enseignant',
                   'Note_Devoir', 'Note_Examen', 'Note_Finale', 'Reussite',
                   'Date_Devoir', 'Date_Examen', 'Session',
                   'Coefficient_Devoir', 'Coefficient_Examen']
        
        df = df[colonnes]
        
        return df 
    
    def save_to_csv(self, df, filename='data/raw/notes_epl.csv'):
        """Sauvegarde le dataset en CSV"""
        # Créer le dossier si nécessaire
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"\n💾 Dataset sauvegardé dans {filename}")
        
        # Sauvegarder aussi un résumé statistique
        summary_filename = 'data/processed'
        self.save_statistical_summary(df, summary_filename)
        
        # Sauvegarder aussi le dictionnaire des UE et matières
        self.save_ue_matiere_dictionnary()
        
        # Sauvegarder la distribution des étudiants par département
        self.save_distribution_report(df)
        
        return filename
    
    def save_distribution_report(self, df):
        """Sauvegarde un rapport sur la distribution des étudiants"""
        # Compter le nombre d'étudiants uniques par département
        etudiants_uniques = df[['ID_Etudiant', 'Departement']].drop_duplicates()
        distribution = etudiants_uniques['Departement'].value_counts()
        
        distribution_df = pd.DataFrame({
            'Departement': distribution.index,
            'Nombre_Etudiants': distribution.values,
            'Pourcentage': (distribution.values / len(etudiants_uniques) * 100).round(2)
        })
        
        # Ajouter les probabilités cibles
        target_distribution = pd.DataFrame({
            'Departement': list(self.departement_distribution.keys()),
            'Probabilite_Cible': [self.departement_distribution[d]*100 for d in self.departement_distribution.keys()]
        })
        
        # Fusionner les deux dataframes
        distribution_report = pd.merge(distribution_df, target_distribution, on='Departement', how='left')
        distribution_report['Difference'] = distribution_report['Pourcentage'] - distribution_report['Probabilite_Cible']
        
        # Sauvegarder le rapport
        dist_filename = 'data/processed/distribution_etudiants.csv'
        distribution_report.to_csv(dist_filename, index=False, encoding='utf-8')
        
        print(f"📊 Rapport de distribution sauvegardé dans {dist_filename}")
        print("\nDistribution réelle des étudiants:")
        print(distribution_report)
    
    def save_statistical_summary(self, df, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        """Sauvegarde un résumé statistique"""
        # Statistiques par département
        stats_departement = df.groupby('Departement').agg({
            'Note_Finale': ['mean', 'median', 'std', 'count', 'min', 'max', 'var'],
            'Reussite': 'mean'
        }).round(2)
        
        # Statistiques par UE
        stats_ue = df.groupby(['Code_UE', 'Nom_UE']).agg({
            'Note_Finale': ['mean', 'median', 'std', 'count', 'min', 'max', 'var'],
            'Reussite': 'mean'
        }).round(2)
        
        # Statistiques par matière
        stats_matiere = df.groupby(['Code_Matiere', 'Matiere']).agg({
            'Note_Finale': ['mean', 'median', 'std', 'count', 'min', 'max', 'var'],
            'Reussite': 'mean'
        }).round(2)

        filepath = os.path.join(output_dir, 'statistiques_resume.xlsx')
        
        # Écrire dans un fichier Excel avec plusieurs onglets
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            stats_departement.to_excel(writer, sheet_name='Par_Departement')
            stats_ue.to_excel(writer, sheet_name='Par_UE')
            stats_matiere.to_excel(writer, sheet_name='Par_Matiere')
            
            # Ajouter les statistiques globales
            stats_global = pd.DataFrame({
                'Statistique': ['Nombre_etudiants', 'Nombre_notes', 'Moyenne_finale', 
                               'Taux_reussite', 'Moyenne_devoir', 'Moyenne_examen',
                               'Nombre_UE_uniques', 'Nombre_matieres_uniques'],
                'Valeur': [
                    df['ID_Etudiant'].nunique(),
                    len(df),
                    df['Note_Finale'].mean(),
                    df['Reussite'].mean() * 100,
                    df['Note_Devoir'].mean(),
                    df['Note_Examen'].mean(),
                    df['Code_UE'].nunique(),
                    df['Code_Matiere'].nunique()
                ]
            })
            stats_global.to_excel(writer, sheet_name='Statistiques_Globales', index=False)
        
        print(f"📊 Résumé statistique sauvegardé dans {filepath}")
    
    def save_ue_matiere_dictionnary(self):
        """Sauvegarde le dictionnaire des UE et matières"""
        ue_matiere_data = []
        
        for dept, dept_data in self.structure.items():
            for filiere, ue_dict in dept_data['ue'].items():
                for ue_code, ue_content in ue_dict.items():
                    ue_nom = ue_content[0]
                    for i, matiere in enumerate(ue_content[1:], 1):
                        code_matiere = self.get_matiere_code(ue_code, i)
                        ue_matiere_data.append({
                            'Departement': dept,
                            'Filiere': filiere,
                            'Code_UE': ue_code,
                            'Nom_UE': ue_nom,
                            'Code_Matiere': code_matiere,
                            'Matiere': matiere,
                            'Ordre_Matiere': i
                        })
        
        df_dict = pd.DataFrame(ue_matiere_data)
        dict_filename = 'data/processed/dictionnaire_ue_matiere.csv'
        df_dict.to_csv(dict_filename, index=False, encoding='utf-8')
        print(f"📚 Dictionnaire UE/Matière sauvegardé dans {dict_filename}")

# Utilisation
if __name__ == "__main__":
    print("=" * 60)
    print("GÉNÉRATEUR DE NOTES DÉTAILLÉES - EPL")
    print("=" * 60)

    print("Sélectionne un département pour un étudiant selon plusieurs méthodes possibles")
    print("Méthodes disponibles:")
    print("1. 'fixed' : Distribution fixe avec probabilités prédéfinies")
    print("2. 'random' : Distribution uniforme complètement aléatoire")
    print("3. 'seasonal' : Variation selon la 'saison ou vague d'inscription' (position de l'étudiant)")
    print("4. 'mixed' : Combinaison des méthodes")

    choix = input("\nVotre choix : ").strip()
    
    generator = DataGenerator(n_etudiants=2000)
    if choix == "1":
        df = generator.generate_dataset(method='fixed')
    elif choix == "2":
        df = generator.generate_dataset(method='random')
    elif choix == "3":
        df = generator.generate_dataset(method='seasonal')
    else:
        df = generator.generate_dataset()
    
    # Sauvegarder les données
    generator.save_to_csv(df)
    
    # Afficher un échantillon des données
    print("\n📋 Échantillon des données générées:")
    print(df[['ID_Etudiant', 'Departement', 'Code_UE', 'Nom_UE', 
              'Code_Matiere', 'Matiere', 'Note_Finale', 'Reussite']].head(10))
    
    # Afficher quelques exemples de codes UE et matières
    print("\n📚 Exemples de codes UE et matières générés:")
    print("=" * 80)
    print(f"Exemple 1 - UE: INF2101 (Algorithmique Avancée)")
    print(f"  Matières: 1INF2101, 2INF2101, 3INF2101")
   