from flask import Blueprint, render_template, g, session, redirect, url_for, request, flash
from decorators import user_login_required,day_limit
from game import utils, main
from models import Day, Game, User
from exts import db

bp = Blueprint("home", __name__, url_prefix='/home')


@bp.route("/index")
@user_login_required
@day_limit
def index():
    data = []
    day_id = session.get("day_id")
    day = Day.query.get(day_id)
    home_type = day.home_type
    if home_type:
        if home_type == 1:
            data.append('流动餐车')
        elif home_type == 2:
            data.append('大众连锁店')
        elif home_type == 3:
            data.append('商场连锁店')
        data.append(day.equipment_value)
        data.append(day.fit_up_value)
    else:
        data.append('尚未选择')
        data.append(0)
        data.append(0)

    return render_template('home_select.html',data=data)


@bp.route("/<int:home_type>")
@user_login_required
@day_limit
def home_select(home_type):
    day_number = session.get("day_number")
    if day_number == 1:
        day_id = session.get("day_id")
        day = Day.query.get(day_id)
        if day.home_type:
            flash("暂不支持变更")
        else:
            day.home_type = home_type
            day.home_pay_day = 0
            if home_type == 1:
                equipment_value = 10000
                fit_up_value = 0
            elif home_type == 2:
                equipment_value = 15000
                fit_up_value = 18000
            elif home_type == 3:
                equipment_value = 22000
                fit_up_value = 38000
            day.equipment_value = equipment_value
            day.fit_up_value = fit_up_value

            resource = session.get("resource")
            resource[4] = resource[4] - equipment_value - fit_up_value
            session['resource'] = resource
            day.cash = resource[4]
            db.session.commit()
            if home_type == 1:
                flash("你已选择流动餐车，剩余现金60000元，工资和租金在营业时优先扣除！")
            if home_type == 2:
                flash("你已选择大众连锁店，剩余现金37000元，工资和租金在营业时优先扣除！")
            if home_type == 3:
                flash("你已选择商场连锁店，剩余现金10000元，工资和租金在营业时优先扣除！")
            return redirect(url_for('play.start'))
    else:
        flash("暂不支持变更")
    return redirect(url_for('home.index'))
