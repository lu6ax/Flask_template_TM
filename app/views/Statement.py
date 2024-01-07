from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db
import os
from app.utils import login_required


Statement_bp = Blueprint('Statement', __name__, url_prefix='/statement')
@login_required

@Statement_bp.route('/home', methods=( 'GET' ,'POST' ))
def defhometabel():
    db = get_db()
    user_id = session.get('user_id')
    if user_id is None :
        g.user = None
        return render_template('auth/login.html')
    else:
        return render_template('Statement/Statement.html')
    actions = db.execute('SELECT * FROM Actifs WHERE IDClient = ? AND IDAction IS NOT NULL', (user_id,)).fetchall()
