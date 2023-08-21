# ML Project DSTI

## Install env 
### With Conda
* Open conda terminal
* Change your directory to location of project : ``cd ...``
* Use this command : ``conda env create -f environment.yml``
* Now you can activate it : ``conda activate dsti_project_ml`` or use it in IDE (restart computer to see it as kernel in VSCode)

### Other way

You can use requirements.txt to create env (with venv or poetry)

# This project is split in 4 parts :

* ``get_data_openlibrary.ipynb`` : Get new data from open library
* ``process_tags.ipynb`` : Creating tags for each books 
* ``data_cleaning_and_eda.ipynb`` : Cleaning data ,handling missing value and EDA (Exploratory_Data_Analysis)
* ``feature_engineering_and_models.ipynb`` : Feature engineering from creating new colomns, modify existing one for fitting in models and trying some models

* ``project.ipynb`` : First notebook of the project, doomed to disappear
