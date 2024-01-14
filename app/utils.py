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

def GetImmeuble():
    db = get_db()
    user_id = session.get('user_id')

    # Récupération des IDImmeuble
    immeuble_ids = db.execute('SELECT IDImmeuble FROM Actifs WHERE IDClient = ?', (user_id,)).fetchall()
    immeuble_ids_list = [id['IDImmeuble'] for id in immeuble_ids]

    # Récupération des noms et des IDs des immeubles
    immeubles = []
    for id in immeuble_ids_list:
        immeuble = db.execute('SELECT ID, Nom FROM Immeubles WHERE ID = ?', (id,)).fetchone()
        if immeuble:
            immeubles.append((immeuble['ID'], immeuble['Nom']))  # Tuple (ID, Nom)

    return immeubles

