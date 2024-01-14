from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db
import os

from app.utils import login_required


AddType_bp = Blueprint('AddType', __name__, url_prefix='/AddType')
@login_required


#route pour séléctionner son type d'actif
@AddType_bp.route('/Choose_type', methods=('GET', 'POST'))
def Choose_type():

    if request.method == 'POST':
        selected_type = request.form.get('selected_type')
        # redirection de l'utilisateur sur la bonne route
        if selected_type == 'Action':
            return redirect(url_for('AddAc.AddActiontodb'))
        elif selected_type == 'Appartement':
            return redirect(url_for('AddAp.AddAppartementtodb'))
        elif selected_type == 'compte':
            return redirect(url_for('Add_Compte'))
        elif selected_type == 'Cryptomonnaie':
            return redirect(url_for('Add_Cryptomonnaie'))
        elif selected_type == 'Immeuble':
            return redirect(url_for('Add_Immeuble'))
        elif selected_type == 'Obligation':
            return redirect(url_for('Add_Obligation'))
        #else:
            return render_template('Add_Type/Choose_type.html')
    
    return render_template('Add_Type/Choose_type.html') 