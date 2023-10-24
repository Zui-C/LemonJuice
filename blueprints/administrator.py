from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    session,
    g
)
from models import Admins,Class,User,Game,Day
from .forms import AdminLoginForm,ClassCreateForm
from werkzeug.security import generate_password_hash,check_password_hash
from decorators import admin_login_required
from exts import db
import json
from blueprints.play import reload

bp = Blueprint("admin", __name__, url_prefix ="/admin")

@bp.route("/admin_login/",methods=['GET','POST'])
def admin_login():
    if request.method == 'GET':
        return render_template("admin_login.html")
    else:
        form = AdminLoginForm(request.form)
        if form.validate():
            admin_name = form.admin_name.data
            admin_password = form.admin_password.data
            admin = Admins.query.filter_by(admin_name=admin_name).first()
            if admin and check_password_hash(admin.admin_password,admin_password):
                session['admin_id'] = admin.id
                return redirect(url_for("admin.class_manage"))
            else:
                flash("用户名和密码不匹配")
                return redirect(url_for("admin.admin_login"))
        else:
            flash("用户名或密码格式不正确")
            return redirect(url_for("admin.admin_login"))

@bp.route("/admin_logout/")
def admin_logout():
    session.clear()
    return redirect(url_for('admin.admin_login'))

@bp.route("/class_manage/")
@admin_login_required
def class_manage():
    return render_template('admin_class_manage.html')


@bp.route("/create_class/",methods=['GET','POST'])
@admin_login_required
def create_class():
    if request.method == 'GET':
        return render_template("admin_create_class.html")
    else:
        form = ClassCreateForm(request.form)
        if form.validate():
            class_name = form.class_name.data
            class_password = form.class_password.data
            confirm_class_password = form.confirm_class_password.data
            class_type = form.class_type.data
            class_obj = Class.query.filter_by(class_name=class_name).first()
            if class_obj:
                flash("该课程代号已存在")
                return redirect(url_for("admin.create_class"))
            else:
                if class_password != confirm_class_password:
                    flash("两次密码不同")
                    return redirect(url_for("admin.create_class"))
                else:
                    hash_class_password = generate_password_hash(class_password)
                    new_class_obj = Class(class_name=class_name,class_password=hash_class_password,class_type=class_type)
                    db.session.add(new_class_obj)
                    db.session.commit()
                    return redirect(url_for("admin.create_class"))
        else:
            flash("输入格式不正确")
            return redirect(url_for("admin.create_class"))



@bp.route("/search_class/")
@admin_login_required
def search_class():
    search_classes = Class.query.order_by(db.text('-create_time')).all()
    return render_template('admin_search_class.html', search_classes=search_classes)


@bp.route("/std_pg/<int:user_id>/")
@admin_login_required
def std_pg(user_id):
    session['user_id'] = user_id
    return reload()


@bp.route("/class_details/<int:class_id>/<int:order>/")
@admin_login_required
def class_details(class_id,order):

    # 创建要显示在表格中的data 字典的list
    data = []

    # 根据class_id 确定 class
    class_obj = Class.query.get(class_id)
    # 显示class_name,endday
    class_name = class_obj.class_name
    end_day = request.args.get('end_day')
    if end_day:
        class_obj.end_day = end_day
        db.session.commit()
    else:
        end_day = class_obj.end_day

    # 根据class 找到 class 的所有user
    users = User.query.filter_by(class_id=class_id).all()
    # 显示学生数量
    users_number = len(users)
    if users_number == 0:
        return render_template('admin_class_details.html', class_name=class_name, users_number=users_number,end_day=end_day)
    # 遍历user填充表格
    for user in users:
        # 单行以列表形式输入
        data_item = {}

        data_item['c1'] = str(user.user_name)
        data_item['c2'] = user.game_number

        # 根据游戏次数及user_id找到最后一次的Game
        game = Game.query.filter_by(user_id=user.id).filter_by(user_game_number=user.game_number).first()
        if_end = "已终止" if game.is_end else "进行中"

        # 显示当前game 的天数 由于会自动创建 默认新一天的购买不算
        current_day_number = game.current_day_number - 1
        data_item['c3'] = current_day_number + 1

        # 根据天数 找到对应的那一天
        day = Day.query.filter_by(game_id=game.id).filter_by(day_number=current_day_number).first()
        # 显示day的信息

        # 一些监控信息
        # 口碑
        data_item['c4'] = round(100*float(day.popularity),2)
        # 现金
        data_item['c5'] = day.cash

        # 一些指标信息
        data_item['c6'] = float(day.profit_sum)

        if day.revenue_sum:
            ngpm =round(100*day.profit_sum/day.revenue_sum,2)
        else:
            ngpm = 0

        data_item['c7'] = float(ngpm)
        roe = round(100*day.profit_sum/(70000),2)
        data_item['c8'] = float(roe)
        data_item['c9'] = day.revenue_sum


        game_number = user.game_number
        games = Game.query.filter_by(user_id=user.id).all()
        sum_profit = 0
        for game in games:
            if game.is_end:
                sum_profit += game.game_profit
            else:
                sum_profit += day.total_value - 70000
        roe = round(sum_profit / (game_number * 700),2)
        data_item['c10'] = roe



        days = Day.query.filter_by(game_id=game.id).order_by(Day.day_number).all()
        sum_cost = 0
        for day in days[1:-1]:
            if day.lemon_cost and day.sugar_cost and day.ice_cost and day.cup_cost:
                sum_cost += day.lemon_cost + day.sugar_cost + day.ice_cost + day.cup_cost
            else:
                sum_cost = 0

        if day.revenue_sum:
            gpm = round(100*(day.revenue_sum-sum_cost)/day.revenue_sum,2)
        else:
            gpm = 0
        data_item['c11'] = float(gpm)

        data_item['c12'] = user.id
        data_item['c13'] = if_end

        data.append(data_item)

    order_num = list(data[0].keys())[order - 1]
    order_data = sorted(data, key=lambda x: x[order_num],reverse=True)

    data = json.dumps(order_data, separators=(',', ':'))

    order_name = {2:'创业次数',
                  3:'当前周数',
                  4: '口碑',
                  5: '现金',
                  6: '累积利润',
                  7: '净利率',
                  8: 'ROE',
                  9: '累积营收',
                  10: '总ROE',
                  11: '毛利率'
                  }[order]
    return render_template('admin_class_details.html',class_name=class_name,users_number=users_number,data=data,order_name=order_name,end_day=end_day)

