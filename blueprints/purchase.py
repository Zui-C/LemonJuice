from flask import Blueprint, render_template, g, session, redirect, url_for, request, flash
from decorators import user_login_required,day_limit
from .forms import PurchaseForm, RecipeForm
from game import utils, main
from models import Day, Game, User
from exts import db

bp = Blueprint("purchase", __name__, url_prefix='/purchase')


@bp.route("/index")
@user_login_required
@day_limit
def index():
    return render_template('purchase.html')


@bp.route("/<item>/<int:bundle>")
@user_login_required
@day_limit
def purchase(item,bundle):
    day_number = session.get("day_number")
    if day_number == 1:
        day_id = session.get("day_id")
        day = Day.query.get(day_id)
        home_type = day.home_type
        if not home_type:
            flash('请先购置店铺！')
            return redirect(url_for('home.index'))

    item_i = [i for i, j in enumerate(['l', 's', 'i', 'c']) if j == item][0]
    item_func = [utils.buy_lemon,utils.buy_sugar,utils.buy_ice,utils.buy_cup]
    func = item_func[item_i]
    if bundle == 0:
        pass
    else:
        bundles = [0,0,0]
        bundles[bundle-1] = 1
        resource = func(g.resource, bundles)
        if resource:
            session['resource'] = resource
            # 数据库更新
            day_id = session.get("day_id")
            day = Day.query.get(day_id)
            day.lemon, day.sugar, day.ice, day.cup, day.cash = resource
            day.purchase += f'{item}{bundles}-'
            db.session.commit()
        else:
            flash("余额不足")
    return redirect(url_for('purchase.index'))
