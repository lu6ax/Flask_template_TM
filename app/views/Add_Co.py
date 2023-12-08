from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db
import os

from app.utils import login_required

AddCo_bp = Blueprint('Add Compte', __name__, url_prefix='/Add-Co')

@login_required

@AddCo_bp.route('/NewCo', methods=( 'GET' ,'POST' ))
def AddComptetodb():

    if request.method == 'POST':

        # On récupère les champs de l'action dans la requête HTTP
        Nom = request.form['Nom']
        Solde = request.form['Solde']
        IBAN = request.form['IBAN']
        
    #changement à effectuer au niveau de la db afin de remplacer les clés étrangères IBAN par No afin d'éviter que si deux utilisateur différent ajoute le même compte la base plante

       
        
        db = get_db()

        
        if Nom and Solde and IBAN :
            try:
                db.execute("INSERT INTO Compte (Nom, Solde, IBAN) VALUES (?, ?, ?)",(Nom, Solde, IBAN))
                # validation de la modification de la base de données
                db.commit()
            except db.IntegrityError:

                # La fonction flash dans Flask est utilisée pour stocker un message dans la session de l'utilisateur
                # dans le but de l'afficher ultérieurement, généralement sur la page suivante après une redirection
                error = "Veuillez vérifier les informations fournies, certaines valeurs ne sont pas adaptées."
                flash(error)
                return redirect(url_for("Add-Co.NewCo"))
            
            return redirect(url_for("home"))
         
        else:
            error = "Veuillez indiquer toutes les informations nécéssaire."
            flash(error)
            return redirect(url_for("Add-Ac.NewAc"))
    else:
        # Si aucune donnée de formulaire n'est envoyée, on affiche le formulaire d'inscription
        return render_template('Add-Co/NewCo.html')
