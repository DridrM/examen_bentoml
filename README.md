# Examen BentoML

Ce repertoire contient l'architecture basique afin de rendre l'évaluation pour l'examen BentoML.

Vous êtes libres d'ajouter d'autres dossiers ou fichiers si vous jugez utile de le faire.

Voici comment est construit le dossier de rendu de l'examen:

```bash       
├── examen_bentoml          
│   ├── data       
│   │   ├── processed      
│   │   └── raw           
│   ├── models      
│   ├── src       
│   └── README.md
```

Afin de pouvoir commencer le projet vous devez suivre les étapes suivantes:

- Forker le projet sur votre compte github

- Cloner le projet sur votre machine

- Récuperer le jeu de données à partir du lien suivant: [Lien de téléchargement]( https://datascientest.s3-eu-west-1.amazonaws.com/examen_bentoml/admissions.csv)


## Installer le projet

1. Installer UV

'''
curl -LsSf https://astral.sh/uv/install.sh | sh
'''

2. Créer l'environnement virtuel

'''
uv python install 3.12
uv venv
'''

3. Installer les dépendances

'''
uv sync
'''

4. Activer l'environnement virtuel

'''
source .venv/bin/activate 
'''

## Preprocessing des données et entrainement du modèle

1. Télécharger les données

> Les données brutes sont déjà téléchargées normalement.

'''
uv run ./src/examen_bentoml/load_data.py 
'''

2. Préparer les données

'''
uv run ./src/examen_bentoml/prepare_data.py 
'''

3. Entrainer et sauvegarder le modèle

'''
uv run ./src/examen_bentoml/train_model.py
'''

> Le modèle est enregistré dans le Model Store BentoML mais aussi dans le dossier `models/` à la racine du projet.

## Créer le Bento, conteneurizer, servir le modèle et tester

1. Créer le bento

> J'ai utilisé le pyproject.toml pour spécifier le build du bento, mais il y a également un fichier `bentofile_old.yaml` à renommer en `bentofile.yaml` qui est équivalent en termes de spécifications de build.

'''
bentoml build
'''

2. Conteneurizer le bento

> Remplacer le nom et le tag du bento par ceux appropriés en exécutant au préalable `bentoml list`

'''
bentoml containerize examen_bentoml:qi6sf74ihollunc2
'''

3. Lancer le conteneur

'''
docker run -p 3000:3000 examen_bentoml:qi6sf74ihollunc2
'''

4. Effectuer les tests

'''
pytest
'''

5. Créer l'archive

> Au préalable retrouver l'ID du conteneur avec `docker ps -a`

'''
docker export -o exam_bentoml_container.tar 61aaba48acad
'''

## Lancer le conteneur à partir de l'archive et tester

1. Re-créer l'image Docker

'''
docker import exam_bentoml_container.tar
'''

2. Exécuter le conteneur à partir de l'image

/!\ Le conteneur n'est pas exécutable à partir de l'archive car l'archivage n'a pas capturé l'entrypoint du conteneur original, pour une raison inconnue.