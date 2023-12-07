from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db
import os

from app.utils import login_required


AddType_bp = Blueprint('Add_Type', __name__, url_prefix='/Add-Type')
@login_required


#route pour séléctionner son type d'actif
@AddType_bp.route('/choose_type', methods=('GET', 'POST'))
def Choose_type():

    if request.method == 'POST':
        selected_type = request.form.get('selected_type')
        # redirection de l'utilisateur sur la bonne route
        if selected_type == 'type1':
            return redirect(url_for('Add Action'))
        elif selected_type == 'type2':
            return redirect(url_for('Add Appartement'))
        elif selected_type == 'type3':
            return redirect(url_for('Add Compte'))
        elif selected_type == 'type4':
            return redirect(url_for('Add Cryptomonnaie'))
        elif selected_type == 'type5':
            return redirect(url_for('Add Immeuble'))
        elif selected_type == 'type6':
            return redirect(url_for('Add Obligation'))

    return render_template('choose_type.html') 