# Projet de gestion d'un établissement : Cas de l'EPL


## Installation des dépendances
```bash

pip install -r requirements.txt

```

## Génération des données

```bash

python data_generator.py

```

## Lancement de l'application

```bash

python run.py

```


## Lancement du dashboard (streamlit)

```bash

streamlit run src/dashboard.py

```

## Lors de la génération des visuels il peut y avoir besoin de taper la commande suivante:

pip install --upgrade kaleido


#### Le fichier data_generator.py

Je génère la structure du dataset

- La méthode select_departement(self, student_id): Sélectionne un département pour un étudiant selon plusieurs méthodes possibles   1. 'fixed' : Distribution fixe avec probabilités prédéfinies
            2. 'random' : Distribution uniforme complètement aléatoire
            3. 'seasonal' : Variation selon la 'saison' (position de l'étudiant)
            4. 'mixed' : Combinaison des méthodes

## Lien de l'application:

[Dashboard](https://eplstats.streamlit.app/)