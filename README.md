# Basic Flask Application for 3rd Year Gymnasium Students as part of their Maturity Project

## Author
Luc Dafflon, Collège du Sud.

## Description
The current directory is a project for a Flask web application. It serves as an online asset manager.

## How to run the project
1. Create a virtual environment
```bash
python -m venv <VIRTUAL-ENVIRONMENT-NAME>
```

3. Activate the virtual environment
  * Windows users:
```bash
<VIRTUAL-ENVIRONMENT-NAME\Scripts\activate
```
  * MacOS users:
```bash
source <VIRTUAL-ENVIRONMENT-NAME>/bin/activate
```

4. Install the dependencies that are in requirements.txt
```bash
pip install -r requirements.txt
```

5. create a config.py file

  SECRET_KEY=<"VOTRE_CLE_SECRETE">
    For this project, a random hexadecimal key was generated.

  DATABASE= <"VOTRE_BASE_DE_DONNÉES.db">


6. Run the project
```bash
python -m flask run --debug
```
