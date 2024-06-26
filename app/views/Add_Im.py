import uuid
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db
import os

AddIm_bp = Blueprint('AddIm', __name__, url_prefix='/AddIm')


from app.utils import login_required, GetCompte
@login_required

@AddIm_bp.route('/NewIm', methods=( 'GET' ,'POST' ))
def AddImmeubletodb():
    db = get_db()
    user_id = session.get('user_id')
    comptes = GetCompte(db,user_id)

    if request.method == 'POST':

        # On récupère les champs de l'action dans la requête HTTP
        Nom = request.form['Nom']

        Valeur = request.form['Valeur']
        Adresse = request.form['Adresse']
        ValeurLocative = request.form.get('ValeurLocative')
        CompteLie = request.form.get('CompteLie')
        DatesTransfert = request.form.get('DatesTransfert')
        FraisGénéraux = request.form.get('FraisGénéraux')
        
        Loué = request.form.get('Loué') == 'on'  # True si cochée, False sinon
        if Loué == 'on' :
            Gains_mensuel = ValeurLocative
        else :
            Gains_mensuel = 0


       
        
        


        if Nom is not None and Valeur is not None and Adresse is not None and ValeurLocative is not None and FraisGénéraux is not None :
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
                IDImmeuble = str(uuid.uuid4())

                db.execute("INSERT INTO Immeuble (ID, Nom, Adresse, Valeur, ValeurLocative, CompteLié, DatesTransfert, FraisGénéraux, Gains_mensuel) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",(IDImmeuble, Nom, Adresse, Valeur, ValeurLocative, CompteLie, DatesTransfert, FraisGénéraux, Gains_mensuel))
                # validation de la modification de la base de données
                db.commit()
                #             option 2 ?                          last_action_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
                
                
                
            except db.IntegrityError:

                # La fonction flash dans Flask est utilisée pour stocker un message dans la session de l'utilisateur
                # dans le but de l'afficher ultérieurement, généralement sur la page suivante après une redirection
                error = "Veuillez vérifier les informations fournies, certaines valeurs ne sont pas adaptées."
                flash(error)
                return redirect(url_for("AddIm.AddImmeubletodb"))
            

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
                IDActif = str(uuid.uuid4())

        #reprendre ici pour créer élément dans la table de liaison 
            try:
                db.execute("INSERT INTO Actifs (ID, IDClient, IDImmeuble) VALUES (?, ?, ?)",(IDActif,g.user['Numero'], IDImmeuble))#je peux juste mettre g.user non ?
                db.commit()

            except db.IntegrityError :#déveloper
                error = "Veuillez réessayer."
                flash(error)
                return redirect(url_for("AddIm.AddImmeubletodb"))


            return redirect(url_for("Statement.defhometabel"))
         
        else:
            error = "Veuillez indiquer toutes les informations nécéssaire."
            flash(error)
            return redirect(url_for("AddIm.AddImmeubletodb"))
    else:
        # Si aucune donnée de formulaire n'est envoyée, on affiche le formulaire d'inscription
        return render_template('Add_Im/NewIm.html', comptes = comptes)



#méthode deux pour insertion dans la table actif