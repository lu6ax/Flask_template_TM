from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db
import os
import uuid
from app.utils import login_required, GetImmeuble

AddAp_bp = Blueprint('AddAp', __name__, url_prefix='/AddAp')


@login_required

@AddAp_bp.route('/NewAp', methods=( 'GET' ,'POST' ))



def AddAppartementtodb():
    db = get_db()
    user_id = session.get('user_id')

    immeubles = GetImmeuble(db, user_id)


    if request.method == 'POST':

        # On récupère les champs de l'action dans la requête HTTP
        Nom = request.form['Nom']
        Surface = request.form['Surface']

        pièces = request.form['Pieces']
        Loué = request.form.get('Loué') == 'on' #valeur true false
        ValeurLocative = request.form.get('Valeurlocative')
        valeur = request.form.get('Valeur')
        Frais = request.form.get('Frais')
        Immeublelié = request.form.get('ImmeubleLie')#valeur id
        Adresse = request.form['Adresse']

        

        # On vérifie si frais d'achat, taux et prix d'aquisition sont remplié
        #vérification de immeuble lié
            #à compléter
        if pièces is None :
            pièces = 0

        if ValeurLocative is None :
            ValeurLocative = 0

        if Immeublelié is True :
            IDImmeublelié = request.form.get('listeDeroulante')
            Immeublelié = 'oui'
        else :
            Immeublelié = 'non'
            IDImmeublelié = 'aucun' 

        if Loué == 'on' :
            Loué = 'oui'  
        else : 
            Loué = 'non'

        if Frais is None :
            Frais = 0
        
        
        


        if Nom and pièces and Loué and ValeurLocative and valeur and Frais and Immeublelié and IDImmeublelié :
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
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! changer le type de données acceptées dans la db et ajouter Nom !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                db.execute("INSERT INTO Appartements (No, Pièces, Loué, ValeuLlocative, Valeur, Frais, NoImmeuble, Nom, Surface) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",(IDappartement, pièces, Loué, ValeurLocative, valeur, Frais, IDImmeublelié, Nom, Surface))
                # validation de la modification de la base de données
                db.commit()
                #             option 2 ?                          last_action_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
                
                
                
            except db.IntegrityError:

                # La fonction flash dans Flask est utilisée pour stocker un message dans la session de l'utilisateur
                # dans le but de l'afficher ultérieurement, généralement sur la page suivante après une redirection
                error = "Veuillez vérifier les informations fournies, certaines valeurs ne sont pas adaptées."
                flash(error)
                return redirect(url_for("AddAp.AddAppartementtodb"))
            

            db = get_db()

        # On récupère l'id de l'utilisateur stocké dans le cookie session
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
            IDActif = str(uuid.uuid4())
        #reprendre ici pour créer élément dans la table de liaison 
            try:
                db.execute("INSERT INTO Actifs (IDClient, IDAppartement, ID) VALUES (?, ?, ?)",(g.user['Numero'], IDappartement, IDActif))#je peux juste mettre g.user non ?
                db.commit()

            except db.IntegrityError :#déveloper
                error = "Veuillez réessayer."
                flash(error)
                return redirect(url_for("AddAp.AddAppartementtodb"))


            return redirect(url_for("Statement.defhometabel"))
         
        else:
            error = "Veuillez indiquer toutes les informations nécéssaire."
            flash(error)
            return redirect(url_for("AddAp.AddAppartementtodb"))
    else:
        # Si aucune donnée de formulaire n'est envoyée, on affiche le formulaire d'inscription
        return render_template('Add_Ap/NewAp.html', immeubles=immeubles)



#méthode deux pour insertion dans la table actif