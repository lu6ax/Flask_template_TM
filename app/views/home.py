from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

# Routes /...
home_bp = Blueprint('home', __name__)



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