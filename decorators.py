from flask import g,redirect,url_for,session,render_template,flash
from functools import wraps
from models import User,Class,Game

def admin_login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if hasattr(g,'admin'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('admin.admin_login'))
    return wrapper

def user_login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if hasattr(g,'user'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('user.user_login'))
    return wrapper

def day_limit(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        game_id = session.get("game_id")
        game = Game.query.get(game_id)
        if game.is_end:
            flash("公司已终止！")
            return redirect(url_for("user.user_details"))
        else:
            return func(*args,**kwargs)
    return wrapper

