from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db
import os

from app.utils import login_required

AddAp_bp = Blueprint('Add Appartement', __name__, url_prefix='/Add-Ap')


@login_required

@AddAc_bp.route('/NewAc', methods=( 'GET' ,'POST' ))
def AddAppartementtodb():

    if request.method == 'POST':

        # On récupère les champs de l'action dans la requête HTTP
        pièces = request.form['pièces']
        Loué = request.form['loué']#valeur true false
        ValeurLocative = request.form['ValeurLocative']
        valeur = request.form.get('valeur')
        Frais = request.form.get('frais')
        Immeublelié = request.form.get('Immeuble')#valeur true false

        

        # On vérifie si frais d'achat, taux et prix d'aquisition sont remplis
        if Immeublelié == True : #demander si c'est mieux "is" ou "=="
            #à compléter

        
        
        


        if pièces and Loué and ValeurLocative and valeur and Frais and Immeublelié:
            try:
                #option 1 :
                
                #lastid = db.execute("SELECT MAX(ID) FROM Action").fetchone()
                #lastidused = lastid[0]

                # Vérifier si des données existent déjà
                #if lastidused is not None:
                    #IDaction = lastidused + 1
                #else:
                # S'il n'y a pas de données, commencer à partir de 1 par exemple
                    #IDaction = 1
                #option3 ->
                IDappartement = str(uuid.uuid4())

                db.execute("INSERT INTO Appartement (No, Pièces, Loué, ValeuLlocative, Valeur, Frais, NoImmeuble) VALUES (?, ?, ?, ?, ?, ?, ?)",(IDappartement, Nom, Valeur, Quantité, Frais_achat, Taux, Prix_acquisition))
                # validation de la modification de la base de données
                db.commit()
                #             option 2 ?                          last_action_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
                
                
                
            except db.IntegrityError:

                # La fonction flash dans Flask est utilisée pour stocker un message dans la session de l'utilisateur
                # dans le but de l'afficher ultérieurement, généralement sur la page suivante après une redirection
                error = "Veuillez vérifier les informations fournies, certaines valeurs ne sont pas adaptées."
                flash(error)
                return redirect(url_for("Add-Ac.NewAc"))
            

            db = get_db()

        # On récupère l'id de l'utilisateur stocké dans le cookie session
            user_id = session.get('user_id')

        # Si l'id de l'utilisateur dans le cookie session est nul, cela signifie que l'utilisateur n'est pas connecté
        # On met donc l'attribut 'user' de l'objet 'g' à None
            if user_id is None:
                g.user = None
                error = "Veuillez vous connecter."
                flash(error)
                return render_template('auth/login.html')

        # Si l'id de l'utilisateur dans le cookie session n'est pas nul, on récupère l'utilisateur correspondant et on stocke
        # l'utilisateur comme un attribut de l'objet 'g'
            else:
            # On récupère la base de données et on récupère l'utilisateur correspondant à l'id stocké dans le cookie session
                db = get_db()
                g.user = db.execute('SELECT * FROM Clients WHERE Numero = ?', (user_id,)).fetchone()

        #reprendre ici pour créer élément dans la table de liaison 
            try:
                db.execute("INSERT INTO Actifs (IDClient, IDAction) VALUES (?, ?)",(g.user['Numero'], IDappartement))#je peux juste mettre g.user non ?
                db.commit()

            except db.IntegrityError :#déveloper
                error = "Veuillez réessayer."
                flash(error)
                return redirect(url_for("Add-Ac.NewAc"))


            return redirect(url_for("home"))
         
        else:
            error = "Veuillez indiquer toutes les informations nécéssaire."
            flash(error)
            return redirect(url_for("Add-Ac.NewAc"))
    else:
        # Si aucune donnée de formulaire n'est envoyée, on affiche le formulaire d'inscription
        return render_template('Add-Ac/NewAc.html')



#méthode deux pour insertion dans la table actif