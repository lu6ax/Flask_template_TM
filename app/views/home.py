from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

from app.db.db import get_db

# Routes /...
home_bp = Blueprint('home', __name__)

# Fonction automatiquement appelée à chaque requête (avant d'entrer dans la route) sur une route appartenant au blueprint 'home_bp' 
# La fonction permet d'ajouter un attribut 'user' représentant l'utilisateur connecté dans l'objet 'g'  
@home_bp.before_app_request 
def load_logged_in_user(): 
 
# On récupère l'id de l'utilisateur stocké dans le cookie session 
    user_id = session.get('user_id') 
    print(user_id) 
 
    # Si l'id de l'utilisateur dans le cookie session est nul, cela signifie que l'utilisateur n'est pas connecté 
    # On met donc l'attribut 'user' de l'objet 'g' à None 
    if user_id is None: 
        g.user = None 
 
    # Si l'id de l'utilisateur dans le cookie session n'est pas nul, on récupère l'utilisateur correspondant et on stocke 
    # l'utilisateur comme un attribut de l'objet 'g' 
    else: 
        # On récupère la base de données et on récupère l'utilisateur correspondant à l'id stocké dans le cookie session 
        db = get_db() 
        g.user = db.execute('SELECT * FROM Clients WHERE Numero = ?', (user_id,)).fetchone() 




# Route /
@home_bp.route('/', methods=('GET', 'POST'))
def landing_page():
    # Affichage de la page principale de l'application
    return render_template('home/index.html')

# Gestionnaire d'erreur 404 pour toutes les routes inconnues
@home_bp.route('/<path:text>', methods=['GET', 'POST'])
def not_found_error(text):
    return render_template('home/404.html'), 404

#if g.user is not None :
@home_bp.route('/logged', methods=('GET', 'POST'))
def home_page():
    # Affichage de la page principale de l'application
    return render_template('home/indexco.html')
#else :
@home_bp.route('/index', methods=('GET', 'POST'))
def uncohomepage():
    return render_template('home/index.html')