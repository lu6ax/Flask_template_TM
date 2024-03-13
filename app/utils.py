import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db

# Ce décorateur est utilisé dans l'application Flask pour protéger certaines vues (routes)
# afin de s'assurer qu'un utilisateur est connecté avant d'accéder à une route 

def login_required(view):
    @functools.wraps(view)

    def wrapped_view(**kwargs):
    
        # Si l'utilisateur n'est pas connecté, il ne peut pas accéder à la route, il faut le rediriger vers la route auth.login
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view

def GetImmeuble(db, user_id):
    db=get_db()
    g.user = db.execute('SELECT * FROM Clients WHERE Numero = ?', (user_id,)).fetchone()
    Id = g.user['Numero']
    
    immeuble_ids = db.execute('SELECT IDImmeuble FROM Actifs WHERE IDClient = ?', (Id,)).fetchall()
    immeuble_ids_list = [id[0] for id in immeuble_ids]
    
    immeubles = []
    for id in immeuble_ids_list:
        immeuble = db.execute('SELECT ID, Nom FROM Immeuble WHERE ID = ?', (id,)).fetchone()
        if immeuble:
            immeubles.append((immeuble['ID'], immeuble['Nom']))
    return immeubles

#possibilité de créer une commande qui vérifie que aucun n'ID n'est similaire a un ID existant et en recréer un sinon !!!!!!!!!!!!!!!!!!!!!!!!!

def GetCompte(db, user_id):
    db=get_db()
    g.user = db.execute('SELECT * FROM Clients WHERE Numero = ?', (user_id,)).fetchone()
    Id = g.user['Numero']
    print(Id)
    compte_ids = db.execute('SELECT IDCompte FROM Actifs WHERE IDClient = ?', (Id,)).fetchall()
    print(compte_ids)
    compte_ids_list = [id[0] for id in compte_ids]
    print(compte_ids_list)
    comptes = []
    for id in compte_ids_list:
        compte = db.execute('SELECT ID, Nom FROM Comptes WHERE ID = ?', (id,)).fetchone()
        print(compte)
        if compte:
            comptes.append((compte['ID'], compte['Nom']))
    print(comptes)
    return comptes
#regrouper les formule en une seul en mettant comme argument le type de table sur laquelle travailler ou àè l'aide de condition if afin d'obtenier la bonne commande sql
