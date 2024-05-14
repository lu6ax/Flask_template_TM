from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.utils import *

# Routes /user/...
user_bp = Blueprint('user', __name__, url_prefix='/user')

# Route /user/profile accessible uniquement à un utilisateur connecté grâce au décorateur @login_required
@user_bp.route('/profile', methods=('GET', 'POST'))
@login_required 
def show_profile():
    # Affichage de la page principale de l'application
    return render_template('user/profile.html')

@user_bp.route('/updateUser', methods=['POST'])
@login_required 
def updateUser():
    db = get_db()
    user_id = session.get('user_id')

    username = request.form.get('AdresseMail')
    password = request.form.get('password')
    date_naissance = request.form.get('DateNaissance')
    nom = request.form.get('Nom')
    prenom = request.form.get('Prenom')

    if not user_id or not username or not nom or not prenom:
        print(user_id,username,nom,prenom)
        flash("Les informations utilisateur sont incomplètes.", 'error')
        return redirect(url_for('user.show_profile'))

    # Construire la requête de mise à jour
    updates = {
        'AdresseMail': username,
        'DateNaissance': date_naissance,
        'Nom': nom,
        'Prenom': prenom
    }

    # Ajouter le mot de passe s'il est fourni et non vide
    if password:
        updates['MotDePasse'] = password

    set_clause = ', '.join([f"{key} = ?" for key in updates.keys()])
    query = f"UPDATE Clients SET {set_clause} WHERE Numero = ?"
    values = list(updates.values()) + [user_id]

    try:
        db.execute(query, values)
        db.commit()
        flash('Utilisateur mis à jour avec succès.', 'success')
    except Exception as e:
        flash(f'Erreur lors de la mise à jour de l\'utilisateur : {e}', 'error')

    
    return redirect(url_for('user.show_profile'))
