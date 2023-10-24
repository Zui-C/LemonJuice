from flask import Blueprint, render_template, request, url_for, redirect, flash, session,g
from exts import db
from game import utils
from .forms import RecipeForm
from decorators import user_login_required,day_limit
from models import Day

bp = Blueprint("recipe", __name__, url_prefix ="/recipe")

@bp.route("/recipe", methods=['GET', 'POST'])
@user_login_required
@day_limit
def recipe():
    recipe = session.get("recipe")
    if recipe:
        g.recipe = recipe
        g.cost = utils.cal_cost(recipe)
    if request.method == 'GET':
        return render_template('recipe.html')
    else:
        form = RecipeForm(request.form)
        if form.validate():
            lemon_per_cup = form.lemon_per_cup.data
            sugar_per_cup = form.sugar_per_cup.data
            ice_per_cup = form.ice_per_cup.data
            price_per_cup = form.price_per_cup.data
            recipe = [lemon_per_cup, sugar_per_cup, ice_per_cup, price_per_cup]
            g.recipe = recipe
            session['recipe'] = recipe
            g.cost = utils.cal_cost(recipe)

            # 数据库更新
            day_id = session.get("day_id")
            day = Day.query.get(day_id)
            day.lemon_per_cup, day.sugar_per_cup, day.ice_per_cup, day.price_per_cup = recipe
            db.session.commit()
        return redirect(url_for("play.start"))
