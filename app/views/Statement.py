from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db
import os
from app.utils import login_required


Statement_bp = Blueprint('Statement', __name__, url_prefix='/statement')
@login_required

@Statement_bp.route('/home', methods=( 'GET' ,'POST' ))

def defhometabel():
    user_id = session.get('user_id')
    db = get_db()
    
    if user_id is None:
        return render_template('auth/login.html')

    # tous les actifs pour l'utilisateur
    try:
        actifs = db.execute('SELECT * FROM Actifs WHERE IDClient = ?', (user_id,)).fetchall()
        print(f"Actifs récupérés: {actifs}")  # Débogage
    except Exception as e:
        print(f"Erreur lors de la récupération des actifs: {e}")
        return render_template('404.html', error=str(e))  

    # actifs par type
    actifs_organises = organiser_actifs_par_type(actifs)
    print(f"Actifs organisés: {actifs_organises}")

    # Récupération des informations détaillées pour chaque actif
    for type_actif, actifs_dans_groupe in actifs_organises.items():
        for i, actif in enumerate(actifs_dans_groupe):
            actifs_organises[type_actif][i] = recuperer_details(actif, type_actif)
    print(f"Actifs avec détails: {actifs_organises}")

    return render_template('Statement/Statement.html', actifs_organises=actifs_organises)

def organiser_actifs_par_type(actifs):
    actifs_organises = {'Comptes': [],'Immeuble': [],'Appartements': [], 'Actions': [], 'Obligation': [], 'Cryptomonnaie': []}  # Initialisez selon les types que vous avez
    for actif in actifs:
        if actif['IDImmeuble']:
            actifs_organises['Immeuble'].append(actif)
        elif actif['IDAction']:
            actifs_organises['Actions'].append(actif)
        elif actif['IDObligation']:
            actifs_organises['Obligation'].append(actif)
        elif actif['IDCompte']:
            actifs_organises['Comptes'].append(actif)
        elif actif['IDAppartement']:
            actifs_organises['Appartements'].append(actif)
        elif actif['IDCryptomonnaie']:
            actifs_organises['Cryptomonnaie'].append(actif)
    return actifs_organises

def recuperer_details(actif, type_actif):
    db = get_db()  # Utilisation de la connexion DB existante
    detail = None
    
    try:
        if type_actif == 'Immeuble':
            # Gardez votre logique existante pour les immeubles si nécessaire
            detail = db.execute('SELECT Nom, Adresse, Valeur, DatesTransfert, FraisGénéraux, Gains_mensuel FROM Immeuble WHERE ID = ?', (actif['IDImmeuble'],)).fetchone()
            if detail is not None:
                try:
                    Immeuble = db.execute("SELECT CompteLié FROM Immeuble WHERE ID = ?", (actif['IDImmeuble'],)).fetchone()
                    if Immeuble and 'CompteLié' in Immeuble:
                        iban = db.execute('SELECT IBAN FROM Comptes WHERE ID = ?', (Immeuble['CompteAssocié'],)).fetchone()
                        if iban and 'IBAN' in iban:
                            iban_value = iban['IBAN']
                        else:
                            iban_value = 'aucun'
                    else:
                        iban_value = 'aucun'
                except Exception as e:
                    print(f"Erreur lors de la récupération de l'IBAN: {e}")
                    iban_value = 'aucun'
                detail = {"id": actif['IDImmeuble'],"Nom": detail["Nom"], "Adresse": detail["Adresse"], "Valeur": detail["Valeur"], "Frais liés": detail["FraisGénéraux"], "Gains mensuel moyen": detail["Gains_mensuel"], "Compte relié à l'immeuble": iban_value, "Date des transferts": detail["DatesTransfert"]}
        elif type_actif == 'Actions':
            # Modifiez cette requête pour récupérer uniquement les colonnes nécessaires
            detail = db.execute('SELECT Nom, Valeur, Quantite, Fraisachat, Taux, PrixAquisition FROM Actions WHERE ID = ?', (actif['IDAction'],)).fetchone()
            # Convertissez le résultat en dictionnaire avec les bons champs si le détail est trouvé
            if detail is not None:
                detail = {"id": actif['IDAction'],"Nom": detail["Nom"], "Valeur": detail["Valeur"], "Quantite": detail["Quantite"], "Taux": detail["Taux"], "Prix d'aquisition": detail["PrixAquisition"], "Frais liés": detail["Fraisachat"]}
        elif type_actif == 'Obligation':
            # Gardez votre logique existante pour les obligations si nécessaire
            detail = db.execute("SELECT Nom, TauxInteret, DateEcheance, Montant, Fraisdegarde FROM Obligation WHERE ID = ?", (actif['IDObligation'],)).fetchone()#ajouter frais d'achat
            if detail is not None:
                try:
                    Compte = db.execute("SELECT CompteAssocié FROM Obligation WHERE ID = ?", (actif['IDObligation'],)).fetchone()
                    if Compte and 'CompteAssocié' in Compte:
                        iban = db.execute('SELECT IBAN FROM Comptes WHERE ID = ?', (Compte['CompteAssocié'],)).fetchone()
                        if iban and 'IBAN' in iban:
                            iban_value = iban['IBAN']
                        else:
                            iban_value = 'aucun'
                    else:
                        iban_value = 'aucun'
                except Exception as e:
                    print(f"Erreur lors de la récupération de l'IBAN: {e}")
                    iban_value = 'aucun'
                detail = {"id" : actif['IDObligation'],"Nom": detail["Nom"], "Montant": detail["Montant"], "Taux d'intérêt": detail["TauxInteret"], "Date d'échéance": detail["DateEcheance"], "Compte lié à l'obligation": iban_value, "Frais de garde": detail["Fraisdegarde"]}
        # Ajoutez des conditions pour d'autres types d'actif si nécessaire
        elif type_actif == 'Appartements':
            # Gardez votre logique existante pour les obligations si nécessaire
            detail = db.execute('SELECT Pièces, Loué, ValeuLlocative, Valeur, Frais FROM Appartements WHERE No = ?', (actif['IDAppartement'],)).fetchone()#retravailler no immeuble pour que ça affiche le nom de l'immeuble lié
            if detail is not None:
                try:
                    Immeuble = db.execute("SELECT NoImmeuble FROM Appartements WHERE No = ?", (actif['IDAppartement'],)).fetchone()
                    if Immeuble and 'NoImmeuble' in Immeuble:
                        Immeubles = db.execute('SELECT Nom FROM Immeuble WHERE ID = ?', (Immeuble['NoImmeuble'],)).fetchone()
                        if Immeubles and 'Nom' in Immeubles:
                            Nom = Immeubles['Nom']
                        else:
                            Nom = 'aucun'
                    else:
                        Nom = 'aucun'
                except Exception as e:
                    print(f"Erreur lors de la récupération de l'IBAN: {e}")
                    Nom = 'aucun'
                detail = {"id": actif['IDAppartement'],"Valeur": detail["Valeur"], "Nombre de pièces": detail["Pièces"], "Loué ? ": detail["Loué"], "Valeur locative": detail["ValeuLlocative"], "Immeuble lié à l'appartement": Nom, "Frais moyen": detail["Frais"]}
        elif type_actif == 'Comptes':
            # Gardez votre logique existante pour les obligations si nécessaire
            detail = db.execute('SELECT Nom, Solde, IBAN FROM Comptes WHERE ID = ?', (actif['IDCompte'],)).fetchone()
            if detail is not None:
                detail = {"id": actif['IDCompte'],"Nom": detail["Nom"], "Solde": detail["Solde"], "IBAN": detail["IBAN"]}
        elif type_actif == 'Cryptomonnaie':
            # Gardez votre logique existante pour les obligations si nécessaire
            detail = db.execute('SELECT Nom, Symbole, Cours, Quantite, Fraisliés FROM Cryptomonnaie WHERE ID = ?', (actif['IDCryptomonnaie'],)).fetchone()
            if detail is not None:
                detail = {"id": actif['IDCryptomonnaie'],"Nom": detail["Nom"], "Symbole": detail["Symbole"], "Cours actuel": detail["Cours"], "Quantité": detail["Quantite"], "Frais en lien": detail["Fraisliés"]}
        print(f"Détails récupérés pour {type_actif}: {detail}")
    except Exception as e:
        print(f"Erreur lors de la récupération des détails pour {type_actif}: {e}")
        detail = {}  # Retournez un dictionnaire vide en cas d'erreur

    return detail


# Route pour afficher la page de modification
@Statement_bp.route('/modifyActif')
def modifyActif():
    db = get_db()
    actifId = request.args.get('actifId')  # Utilisez request.args pour les requêtes GET
    typeActif = request.args.get('typeActif')

    tables = ['Comptes', 'Immeuble', 'Actions', 'Appartements', 'Obligation', 'Cryptomonnaie']  
    if typeActif not in tables:
        flash("Type d'actif invalide.", 'error')
        return redirect(url_for('Statement.defhometabel'))

    query = f'SELECT * FROM {typeActif} WHERE id = ?'
    details = db.execute(query, (actifId,)).fetchone()

    if details is None:
        flash("Aucun actif trouvé avec cet ID.", 'error')
        return redirect(url_for('Statement.defhometabel'))

    actifDetails = {column: value for column, value in zip(details.keys(), details)}

    return render_template('ModifynSupress/modify_actif.html', actif=actifDetails, typeActif=typeActif)

@Statement_bp.route('/updateActif', methods=['POST'])
def updateActif():
    # Mettez à jour l'actif dans la base de données avec les nouvelles données reçues
    update_actif(actifId, request.form)
    return redirect(url_for('home'))

# Route pour supprimer un actif
@Statement_bp.route('/deleteActif', methods=( 'GET' ,'POST' ))
def deleteActif():
    db = get_db()

    actifId = request.form['actifId']
    typeActif = request.form['typeActif']
    #pour la suite expliquer les f-string dans le doc écrit
    print(typeActif)
    tables = ['Comptes', 'Immeuble', 'Actions', 'Appartements', 'Obligation', 'Cryptomonnaie']  
    if typeActif not in tables:
        flash('Type d\'actif invalide.', 'error')#inéréssant l'utilisation du / qui évite bcp de perte de temps
        
        return redirect(url_for('Statement.defhometabel'))  

    supp = f'DELETE FROM {typeActif} WHERE id = ?'
    db.execute(supp, (actifId,))
    flash('Actif supprimé avec succès.', 'success')
    return redirect(url_for('Statement.defhometabel'))  

    
    