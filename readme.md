# ML Project DSTI

## Installing environment

### With Conda
* Open conda terminal
* Change your directory to location of project : ``cd ...``
* Use this command : ``conda env create -f environment.yml``
* Now you can activate it : ``conda activate dsti_project_ml`` or use it in IDE (restart computer to see it as kernel in VSCode)

### Other way

You can use requirements.txt to create env (with venv or poetry)

## Repo organization

### Data

The ``data`` folder contains:
* ``books.csv``: our dataset
* ``works.csv``: works ID and their associated ISBN, fetched from OpenLibrary
* ``tags.csv``: tags and their associated work ID, fetched from OpenLibrary
* ``tags_reduced.csv``: processed tags (one-hot encoding, tf-idf, umap)

OpenLibrary data is retrieved through the following notebooks:
* ``get_data_openlibrary.ipynb``: fetch works and tags through OpenLibrary's API
* ``process_tags.ipynb``: tags processing (one-hot encoding, tf-idf, umap)

### Data preprocessing

This part regroups:
* Data cleaning
* Exploratory Data Analysis (EDA)
* Feature Engineering

and is achieved through ``data_preprocessing.ipynb``.

The preprocessed data is then saved into ``books_preprocessed.csv`` inside the ``data_preprocessed`` folder.

### Models

