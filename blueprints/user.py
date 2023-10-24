from flask import Blueprint, render_template, request, url_for, redirect, flash, session,g
from .forms import UserCreateForm
from werkzeug.security import check_password_hash
from models import Class,User,Game,Day
from exts import db
from .play import initialize,reload
from decorators import user_login_required

bp = Blueprint("user", __name__, url_prefix ="/user")


@bp.route("/user_login",methods=['GET','POST'])
def user_login():
    if request.method == 'GET':
        return render_template("user_login.html")
    else:
        form = UserCreateForm(request.form)
        if form.validate():
            class_name = form.class_name.data
            class_password = form.class_password.data
            user_name = form.user_name.data
            first_login_label = form.first_login_label.data
            class_obj = Class.query.filter_by(class_name=class_name).first()

            if class_obj and check_password_hash(class_obj.class_password,class_password):
                # 首次登陆判断昵称是否用过
                if first_login_label:
                    if User.query.filter_by(class_id=class_obj.id).filter_by(user_name=user_name).first():
                        flash("该昵称已存在")
                        return redirect(url_for("user.user_login"))

                    else:
                        new_user = User(user_name=user_name,class_id=class_obj.id,game_number=0)
                        class_obj.class_student_number += 1
                        db.session.add(new_user)
                        db.session.commit()
                        session['user_id'] = new_user.id
                        return initialize()
                else:
                    user = User.query.filter_by(class_id=class_obj.id).filter_by(user_name=user_name).first()
                    if user:
                        session['user_id'] = user.id
                        return reload()
                    else:
                        flash("该昵称不存在")
                        return redirect(url_for("user.user_login"))
            else:
                flash("用户名和密码不匹配")
                return redirect(url_for("user.user_login"))
        else:
            flash("用户名或密码格式不正确")
            return redirect(url_for("user.user_login"))


@bp.route("/user_details")
@user_login_required
def user_details():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    g.game_number = user.game_number

    class_id = user.class_id
    belong_class = Class.query.get(class_id)
    g.max_termination = belong_class.max_termination
    g.end_day = belong_class.end_day
    # 找到所有game
    games = Game.query.filter_by(user_id=user.id).all()

    end_games = []
    on_game = []
    sum_profit = 0
    for game in games:
        if game.is_end:
            end_games.append([game.user_game_number,game.current_day_number,game.game_profit,game.game_profit/700])
            sum_profit += game.game_profit
        else:
            on_game = [game.user_game_number,g.day_number,g.total_value-70000,(g.total_value-70000)/700]
            sum_profit += g.total_value-70000
    g.end_games = end_games
    g.on_game = on_game
    g.sum_profit = sum_profit
    g.roe = sum_profit/(g.game_number*700)
    return render_template("user_details.html")



@bp.route("/user_logout")
def user_logout():
    session.clear()
    return redirect(url_for('user.user_login'))
