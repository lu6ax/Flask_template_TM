from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db
import os
import uuid

from app.utils import login_required

AddCo_bp = Blueprint('AddCo', __name__, url_prefix='/AddCo')

@login_required

@AddCo_bp.route('/NewCo', methods=( 'GET' ,'POST' ))
def AddComptetodb():

    if request.method == 'POST':

        # On récupère les champs de l'action dans la requête HTTP
        Nom = request.form['Nom']
        Solde = request.form['Solde']
        IBAn = request.form['IBAN']
        
    #changement à effectuer au niveau de la db afin de remplacer les clés étrangères IBAN par No afin d'éviter que si deux utilisateur différent ajoute le même compte la base plante

       
        
        db = get_db()

        
        if Nom and Solde and IBAn :

            IDCompte = str(uuid.uuid4())

            try:
                db.execute("INSERT INTO Comptes (Nom, Solde, IBAN, ID) VALUES (?, ?, ?, ?)",(Nom, Solde, IBAn, IDCompte))
                # validation de la modification de la base de données
                db.commit()
            except db.IntegrityError:

                # La fonction flash dans Flask est utilisée pour stocker un message dans la session de l'utilisateur
                # dans le but de l'afficher ultérieurement, généralement sur la page suivante après une redirection
                error = "Veuillez vérifier les informations fournies, certaines valeurs ne sont pas adaptées."
                flash(error)
                return redirect(url_for("AddCo.AddComptetodb"))
            
            user_id = session.get('user_id')

        # Si l'id de l'utilisateur dans le cookie session est nul, cela signifie que l'utilisateur n'est pas connecté
        # On met donc l'attribut 'user' de l'objet 'g' à None
            if user_id is None:
                g.user = None
                error = "Veuillez vous connecter."
                flash(error)
                return url_for('auth.login')

        # Si l'id de l'utilisateur dans le cookie session n'est pas nul, on récupère l'utilisateur correspondant et on stocke
        # l'utilisateur comme un attribut de l'objet 'g'
            else:
            # On récupère la base de données et on récupère l'utilisateur correspondant à l'id stocké dans le cookie session
                db = get_db()
                g.user = db.execute('SELECT * FROM Clients WHERE Numero = ?', (user_id,)).fetchone()
                IDactif = str(uuid.uuid4())

        #reprendre ici pour créer élément dans la table de liaison 
            try:
                db.execute("INSERT INTO Actifs (IDClient, IDCompte, ID) VALUES (?, ?, ?)",(g.user['Numero'], IDCompte, IDactif))#je peux juste mettre g.user non ?
                db.commit()

            except db.IntegrityError :#déveloper
                error = "Veuillez réessayer."
                flash(error)
                return redirect(url_for("AddCo.AddComptetodb"))


            
            return redirect(url_for("Statement.defhometabel"))
         
        else:
            error = "Veuillez indiquer toutes les informations nécéssaire."
            flash(error)
            return redirect(url_for("AddCo.AddComptetodb"))
    else:
        # Si aucune donnée de formulaire n'est envoyée, on affiche le formulaire d'inscription
        return render_template('Add_Co/NewCo.html')

