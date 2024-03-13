import uuid
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db
import os

AddCr_bp = Blueprint('AddCr', __name__, url_prefix='/AddCr')


from app.utils import login_required
@login_required

@AddCr_bp.route('/NewCr', methods=( 'GET' ,'POST' ))
def AddCryptotodb():
    db = get_db()
    user_id = session.get('user_id')

    if request.method == 'POST':

        # On récupère les champs de l'action dans la requête HTTP
        Nom = request.form['Nom']
        
        Symbole = request.form['Symbole']
        Cours = request.form.get('Cours à la piece') 
        Quantité = request.form.get('Quantité')
        Fraisliés = request.form.get('Fraisliés')

        

        # On vérifie si frais d'achat, taux et prix d'aquisition sont remplis
        if Fraisliés is None : #demander si c'est mieux "is" ou "=="
            Fraisliés = 0
        
        
        


        if Nom and Symbole and Quantité and Cours and Fraisliés is not None :
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
                IDCr = str(uuid.uuid4())

                db.execute("INSERT INTO Cryptomonnaie (ID, Nom, Symbole, Quantite, Fraisliés, Cours) VALUES (?, ?, ?, ?, ?, ?)",(IDCr, Nom, Symbole, Quantité, Fraisliés, Cours))
                # validation de la modification de la base de données
                db.commit()
                #             option 2 ?                          last_action_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
                
                
                
            except db.IntegrityError:

                # La fonction flash dans Flask est utilisée pour stocker un message dans la session de l'utilisateur
                # dans le but de l'afficher ultérieurement, généralement sur la page suivante après une redirection
                error = "Veuillez vérifier les informations fournies, certaines valeurs ne sont pas adaptées."
                flash(error)
                return redirect(url_for("Add-Cr.NewCr"))
            

            db = get_db()

        # On récupère l'id de l'utilisateur stocké dans le cookie session
            user_id = session.get('user_id')
            IDActif = str(uuid.uuid4())

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

        #reprendre ici pour créer élément dans la table de liaison 
            try:
                db.execute("INSERT INTO Actifs (IDClient, IDCryptomonnaie, ID) VALUES (?, ?, ?)",(g.user['Numero'], IDCr, IDCr))#je peux juste mettre g.user non ?
                db.commit()

            except db.IntegrityError :#déveloper
                error = "Veuillez réessayer."
                flash(error)
                return redirect(url_for("AddCr.AddCryptotodb"))


            return redirect(url_for("Statement.defhometabel"))
         
        else:
            error = "Veuillez indiquer toutes les informations nécéssaire."
            flash(error)
            return redirect(url_for("Add_Cr.NewCr"))
    else:
        # Si aucune donnée de formulaire n'est envoyée, on affiche le formulaire d'inscription
        return render_template('Add_Cr/NewCr.html')



#méthode deux pour insertion dans la table actif