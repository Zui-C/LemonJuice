from flask import Blueprint, render_template, g, session, redirect, url_for, request, flash
from decorators import user_login_required,day_limit
from game import utils, main
from models import Day, Game, User,Class
from exts import db
import json

bp = Blueprint("play", __name__, url_prefix='/play')

def initialize():
    # 先判断是否超过破产上限
    user_id = session.get("user_id")
    user = User.query.get(user_id)


    # 初始化资源
    resource = [0, 0, 0, 0, 70000]
    session['resource'] = resource
    session['total_value'] = resource[4]

    # 初始化默认配方
    recipe = [3, 3, 10, 10]
    session['recipe'] = recipe
    # 初始化时间
    day_number = 1
    session['day_number'] = day_number
    # 生成温度及天气
    temperature, weather = main.random_day(day_number)
    session['temperature'] = temperature
    session['weather'] = weather
    # 生成初始欢迎程度
    satisfaction = 0
    session['satisfaction'] = satisfaction
    popularity = 0.2
    session['popularity'] = popularity

    # 数据库操作
    user.game_number += 1
    new_game = Game(user_id=user_id, user_game_number=user.game_number, current_day_number=1)
    new_game.day_number = 1

    db.session.add(new_game)
    db.session.commit()
    session['game_id'] = new_game.id

    # 创建第0天
    new_day0 = Day(day_number=0, satisfaction=satisfaction, popularity=popularity, game_id=new_game.id,
                   lemon=resource[0],
                   sugar=resource[1], ice=resource[2], cup=resource[3], cash=resource[4],
                   lemon_value=0, sugar_value=0, ice_value=0,cup_value=0,total_value=resource[4],
                   purchase_people=0,
                   potential_people=0,oper_cost=0,total_cost=0,total_waste_value=0,
                   profit=0,revenue=0,revenue_sum=0,profit_sum=0)
    new_day1 = Day(day_number=1, lemon_per_cup=recipe[0], sugar_per_cup=recipe[1],
                   ice_per_cup=recipe[2], price_per_cup=recipe[3], game_id=new_game.id,
                   lemon=resource[0], sugar=resource[1], ice=resource[2], cup=resource[3],
                   cash=resource[4],lemon_value=0, sugar_value=0, ice_value=0,cup_value=0,total_value=resource[4],
                   weather=weather, temperature=temperature,
                   revenue_sum=0,profit_sum=0)

    db.session.add(new_day0)
    db.session.add(new_day1)
    db.session.commit()
    session['day_id'] = new_day1.id

    return redirect(url_for("play.result"))

def reload():
    # 根据user_id 找user
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    # 根据user_id及game_number找game
    game = Game.query.filter_by(user_id=user_id).filter_by(user_game_number=user.game_number).first()
    # 根据game_id,current_day_number找day
    day = Day.query.filter_by(day_number=game.current_day_number).filter_by(game_id=game.id).first()
    session['game_id'] = game.id
    session['day_id'] = day.id

    # 找到day后读取一下存入的信息
    resource = [day.lemon, day.sugar, day.ice, day.cup, day.cash]
    session['resource'] = resource
    recipe = [day.lemon_per_cup, day.sugar_per_cup, day.ice_per_cup, day.price_per_cup]
    session['recipe'] = recipe

    session['day_number'] = day.day_number
    session['temperature'] = float(day.temperature)
    session['weather'] = day.weather
    session['total_value'] = float(day.total_value)

    last_day = Day.query.filter_by(day_number=game.current_day_number - 1).filter_by(game_id=game.id).first()
    session["purchase_people"] = int(last_day.purchase_people)
    session["potential_people"] = int(last_day.potential_people)
    session['satisfaction'] = float(last_day.satisfaction)
    session['popularity'] = float(last_day.popularity)
    return redirect(url_for("play.result"))

@bp.route("/open_check")
@user_login_required
@day_limit
def open_check():
    day_number = session.get("day_number")
    if day_number == 1:
        day_id = session.get("day_id")
        day = Day.query.get(day_id)
        home_type = day.home_type
        if not home_type:
            flash('请先购置店铺！')
            return redirect(url_for('home.index'))
    recipe = session.get("recipe")
    resource = session.get("resource")
    # 库存控制警告
    max_supply_people = utils.max_supply(recipe.copy(), resource.copy())
    if max_supply_people < 10:
        return render_template('warning.html')
    else:
        return redirect(url_for("play.open"))

@bp.route("/open")
@user_login_required
@day_limit
def open():
    # 检查工资
    day_id = session.get("day_id")
    day = Day.query.get(day_id)
    home_type = day.home_type
    if home_type == 1:
        total_rent_cost = 500
        total_wages_cost = 0
    elif home_type == 2:
        total_rent_cost = 1800
        total_wages_cost = 2000
    elif home_type == 3:
        total_rent_cost = 3500
        total_wages_cost = 4500

    home_pay_day = day.home_pay_day

    resource = session.get("resource")
    if home_pay_day == 0:
        resource[4] = resource[4] - total_rent_cost - total_wages_cost
        if resource[4] < 0:
            flash('你因无法支付房租及工资被破产清算')
            return redirect(url_for("play.end_by_break"))
        day.cash = resource[4]
        next_home_pay_day = 3
        db.session.commit()
    else:
        next_home_pay_day = home_pay_day - 1

    day_number = session.get("day_number")
    recipe = session.get("recipe")
    weather = session.get("weather")
    temperature = session.get("temperature")
    popularity = session.get("popularity")

    # 开门营业  目前直接结算
    resource, purchase_people, potential_people, satisfaction, popularity,lemon_waste,ice_waste,message = \
        main.simulate(home_type, recipe, resource, weather, temperature, popularity)
    session['message'] = message

    # 更新session数值
    session['resource'] = resource
    session['purchase_people'] = purchase_people
    session['potential_people'] = potential_people
    session['satisfaction'] = satisfaction
    session['popularity'] = popularity

    # 数据库更新 以下全部
    day_id = session.get("day_id")
    day = Day.query.get(day_id)
    # 库存价值
    game_id = session.get("game_id")
    last_day = day.query.filter_by(game_id=game_id).filter_by(day_number=day_number - 1).first()
    l1,l2,s1,s2,i1,i2,c1,c2,total = utils.analyse_daily_purchase(day.purchase)

    # 平均库存价值为 之前的价值+购买花费/之前的数量+购买数量
    # 如果有一个不为0则可以计算
    if l1 == 0 and last_day.lemon == 0:
        lemon_value = 0
        lemon_cost = 0
        lemon_waste = 0
        lemon_waste_value =0
    else:
        ev = (last_day.lemon_value+l2)/(last_day.lemon+l1)
        lemon_value = round(ev*resource[0],1)
        lemon_waste_value = round(ev*lemon_waste,1)
        lemon_cost = round(last_day.lemon_value+l2-lemon_value,1) - lemon_waste_value
    day.lemon_waste = lemon_waste
    day.lemon_waste_value = lemon_waste_value
    day.lemon_value = lemon_value
    day.lemon_cost = lemon_cost
    if s1 == 0 and last_day.sugar == 0:
        sugar_value = 0
        sugar_cost = 0
    else:
        ev = (last_day.sugar_value+s2)/(last_day.sugar+s1)
        sugar_value = round(ev*resource[1],1)
        sugar_cost = round(last_day.sugar_value+s2-sugar_value,1)
    day.sugar_value = sugar_value
    day.sugar_cost = sugar_cost

    if i1 == 0:
        ice_value = 0
        ice_cost = 0
        ice_waste = 0
        ice_waste_value = 0
    else:
        ice_value = 0
        ev = i2/i1
        ice_waste_value = round(ev*ice_waste,1)
        ice_cost = round(i2,1) - ice_waste_value
    day.ice_waste = ice_waste
    day.ice_waste_value = ice_waste_value
    day.ice_value = ice_value
    day.ice_cost = ice_cost

    if c1 == 0 and last_day.cup == 0:
        cup_value = 0
        cup_cost = 0
    else:
        ev = (last_day.cup_value+c2)/(last_day.cup+c1)
        cup_value = round(ev*resource[3],1)
        cup_cost = round(last_day.cup_value+c2-cup_value,1)
    day.cup_value = cup_value
    day.cup_cost = cup_cost


    # 营收
    revenue = resource[4] - day.cash
    day.revenue = revenue
    day.revenue_sum = last_day.revenue_sum + revenue

    # 营业成本  物料成本+员工工资+设备摊销
    home_type = day.home_type
    if home_type == 1:
        total_equipment_value = 10000
        total_fit_up_value = 0
    elif home_type == 2:
        total_equipment_value = 15000
        total_fit_up_value = 18000
    elif home_type == 3:
        total_equipment_value = 22000
        total_fit_up_value = 38000

    equipment_cost = round(total_equipment_value/48,1)
    equipment_value = day.equipment_value
    if equipment_value - equipment_cost < 0:
        equipment_cost = equipment_value
        equipment_value = 0
    else:
        equipment_value = equipment_value - equipment_cost
        equipment_cost = equipment_cost
    day.equipment_value = equipment_value
    day.equipment_cost = equipment_cost

    wages_cost = round(total_wages_cost/4,1)
    rent_cost = round(total_rent_cost/4,1)
    day.wages_cost = wages_cost
    day.rent_cost = rent_cost

    # 营业成本 = 物料成本+员工工资+设备摊销
    total_cost = round(lemon_cost + sugar_cost + ice_cost + cup_cost + equipment_cost + wages_cost + rent_cost, 1)
    day.total_cost = total_cost

    # 营业费用
    oper_cost = round(total_fit_up_value/48,1)
    fit_up_value = day.fit_up_value
    if fit_up_value - oper_cost < 0:
        oper_cost = fit_up_value
        fit_up_value = 0
    else:
        fit_up_value = fit_up_value - oper_cost
        oper_cost = oper_cost
    day.fit_up_value = fit_up_value
    day.oper_cost = oper_cost

    # 营业外支出
    total_wast_value = round(lemon_waste_value+ice_waste_value,1)
    day.total_waste_value = total_wast_value

    # 累积利润=营收-营业成本-营业费用-营业外支出
    profit = round(revenue - total_cost - oper_cost - total_wast_value,1)
    day.profit = profit
    day.profit_sum = round(profit + last_day.profit_sum,1)

    # 资产价值 现金+库存价值+设备残值+待摊费用 +现金待摊+房租待摊
    if home_pay_day == 0:
        rent_value = total_rent_cost - rent_cost
        wages_value = total_wages_cost - wages_cost
    else:
        rent_value = day.rent_value - rent_cost
        wages_value = day.wages_value - wages_cost
    day.wages_value = wages_value
    day.rent_value = rent_value

    total_value = round(resource[4] + lemon_value + sugar_value + cup_value + ice_value + equipment_value + fit_up_value + wages_value + rent_value,1)
    day.total_value = total_value
    session['total_value'] = total_value

    day.lemon, day.sugar, day.ice, day.cup, day.cash = resource
    day.purchase_people = purchase_people
    day.potential_people = potential_people
    day.satisfaction = satisfaction
    day.popularity = popularity
    db.session.commit()

    # 加一天
    day_number = day_number + 1
    session['day_number'] = day_number
    # 生成温度及天气
    temperature, weather = main.random_day(day_number)
    session['temperature'] = temperature
    session['weather'] = weather

    game_id = session.get("game_id")
    next_day = Day(day_number=day_number, lemon_per_cup=recipe[0], sugar_per_cup=recipe[1],
                   ice_per_cup=recipe[2], price_per_cup=recipe[3], game_id=game_id,
                   lemon=resource[0], sugar=resource[1], ice=resource[2], cup=resource[3],
                   total_value=total_value,fit_up_value=fit_up_value,equipment_value=equipment_value,
                   rent_value=rent_value,wages_value=wages_value,
                   cash=resource[4], weather=weather, temperature=temperature,
                   home_type=day.home_type,home_pay_day=next_home_pay_day,
                   revenue_sum=day.revenue_sum,profit_sum=day.profit_sum,popularity=popularity)
    game = Game.query.get(game_id)
    game.current_day_number = day_number
    db.session.add(next_day)
    db.session.commit()
    session['day_id'] = next_day.id

    user_id = session.get("user_id")
    user = User.query.get(user_id)
    class_obj = Class.query.get(user.class_id)
    end_day = class_obj.end_day
    # 时间周期走完，公司被收购
    if day_number > end_day:
        return redirect(url_for("play.end_by_buy"))

    if popularity < 0.08:
        flash('你的口碑已低于8%，请注意调整策略！')
    return redirect(url_for("play.result"))

# 开始界面（经营准备
@bp.route("/start")
@user_login_required
@day_limit
def start():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    class_obj = Class.query.get(user.class_id)
    g.end_day = class_obj.end_day
    # 当天信息汇总
    g.day_number = session.get("day_number")
    g.temperature = session.get("temperature")
    weather = session.get("weather")
    weather_chn = utils.weather_trans(weather)
    g.weather = weather_chn
    # 解析购买
    day_id = session.get("day_id")
    day = Day.query.get(day_id)
    g.daily_purchase = utils.analyse_daily_purchase(day.purchase)

    # 更新指标
    g.revenue_sum = day.revenue_sum
    g.profit_sum = day.profit_sum
    g.popularity = session.get("popularity")

    # 解析配方
    g.recipe = session.get("recipe")
    g.cost = utils.cal_cost(g.recipe)
    g.max_supply_people = utils.max_supply(g.recipe.copy(), g.resource.copy())

    data = []
    home_type = day.home_type
    if home_type:
        if home_type == 1:
            data.append('流动餐车')
            rent_cost = '500（管理费）'
            wages_cost = 0
        elif home_type == 2:
            data.append('大众连锁店')
            rent_cost = 1800
            wages_cost = 2000
        elif home_type == 3:
            data.append('商场连锁店')
            rent_cost = 3500
            wages_cost = 4500
        data.append(day.equipment_value)
        data.append(day.fit_up_value)
        data.append(rent_cost)
        data.append(wages_cost)
        g.home_pay_day = day.home_pay_day
    else:
        data.append('尚未选择')
        data.append(0)
        data.append(0)
        data.append(0)
        data.append(0)
        g.home_pay_day = 'N'

    g.data = data

    return render_template('start.html')
# 结果概览
@bp.route("/result")
@user_login_required
def result():
    g.message = session.get('message')
    # 当天信息汇总
    g.day_number = session.get("day_number")
    if g.day_number == 1:
        return render_template('intro.html')

    # 前一经营小结
    g.purchase_people = session.get("purchase_people")
    g.satisfaction = session.get("satisfaction")
    g.popularity = session.get("popularity")

    day_id = session.get("day_id")
    day = Day.query.get(day_id)
    # 读取前一天信息比较
    if g.day_number > 1:
        game_id = session.get("game_id")
        last_day = Day.query.filter_by(game_id=game_id).filter_by(day_number=g.day_number - 1).first()
        g.use = g.purchase_people * last_day.lemon_per_cup, g.purchase_people * last_day.sugar_per_cup, g.purchase_people * last_day.ice_per_cup, g.purchase_people
        g.lemon_waste = last_day.lemon_waste
        g.ice_waste = last_day.ice_waste

        last_last_day = Day.query.filter_by(game_id=game_id).filter_by(day_number=g.day_number - 2).first()

        g.purchase_people_change = g.purchase_people - last_last_day.purchase_people
        g.satisfaction_change = g.satisfaction - float(last_last_day.satisfaction)
        g.popularity_change = g.popularity - float(last_last_day.popularity)


        g.total_cost = round(last_day.total_cost,1)
        g.total_cost_change = round(g.total_cost - last_last_day.total_cost,1)
        g.oper_cost = round(last_day.oper_cost,1)
        g.oper_cost_change = round(g.oper_cost - last_last_day.oper_cost,1)
        g.total_waste_value = round(last_day.total_waste_value,1)
        g.total_waste_value_change = round(g.total_waste_value - last_last_day.total_waste_value,1)
        g.revenue = last_day.revenue
        g.revenue_change = g.revenue - last_last_day.revenue
        g.profit = round(last_day.profit,1)
        g.profit_change = round(g.profit - last_last_day.profit,1)


        # 查询当前进行的游戏
        game_id = session.get("game_id")
        # 获得进行游戏每一天的数据
        days = Day.query.filter_by(game_id=game_id).order_by(Day.day_number).all()
        data = []

        for day in days[1:-1]:
            data_item = {}
            data_item["c1"] = int(day.day_number)
            data_item["c2"] = int(day.profit_sum)
            data_item["c3"] = int(day.revenue_sum)
            data_item["c4"] = round(float(day.satisfaction*100),2)
            data_item["c5"] = round(float(day.popularity*100),2)
            data.append(data_item)

        line3 = []
        line4 = []
        line5 = []
        line6 = []
        dayline = []

        for day in days[1:-1]:
            i = int(day.day_number)
            # if i <= 10:
            line3.append(data[i-1]["c2"])
            line4.append(data[i-1]["c3"])
            dayline.append("Week" + str(i))
            line5.append(data[i-1]["c4"])
            line6.append(data[i-1]["c5"] )

        return render_template('result.html', line3= list(line3), line4= list(line4), dayline= list(dayline), line5= list(line5), line6= list(line6))



# 因收购终止
@bp.route("/end_by_buy")
@user_login_required
@day_limit
def end_by_buy():
    game_id = session.get("game_id")
    game = Game.query.get(game_id)
    game.is_end = 1

    last_day = Day.query.filter_by(game_id=game_id).filter_by(day_number=g.day_number - 1).first()

    g.total_value = last_day.total_value

    popularity = float(last_day.popularity)
    if last_day.home_type == 1:
        g.popularity_value = 0
    elif last_day.home_type == 2:
        g.popularity_value = (popularity - 0.2) * 50000
    elif last_day.home_type == 3:
        g.popularity_value = (popularity - 0.2) * 100000

    g.price = g.total_value + g.popularity_value
    profit = g.price-70000
    g.roe = round(profit/700,2)

    game.game_profit = profit
    db.session.commit()
    return render_template("end_by_buy.html")


# 判断是否要重开
@bp.route("/restart")
@user_login_required
def restart():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    game_number = user.game_number

    class_id = user.class_id
    belong_class = Class.query.get(class_id)
    max_termination = belong_class.max_termination

    if game_number >= max_termination:
        flash("所有机会已用完！")
        return redirect(url_for("user.user_details"))
    else:
        flash(f"你的第{game_number+1}/{max_termination}次创业！")
        return initialize()

# 破产清算
@bp.route("/end_by_break")
@user_login_required
@day_limit
def end_by_break():
    game_id = session.get("game_id")
    game = Game.query.get(game_id)
    game.is_end = 1

    day_id = session.get("day_id")
    day = Day.query.get(day_id)
    g.cash = day.cash
    g.other_value = day.total_value - g.cash
    g.loss = round(g.other_value/2,1)
    g.profit = g.cash + g.other_value - g.loss - 70000
    g.roe = round(g.profit/700,2)

    game.game_profit = g.profit
    db.session.commit()
    return render_template("end_by_break.html")


# 解散清算
@bp.route("/end_by_close")
@user_login_required
@day_limit
def end_by_close():
    game_id = session.get("game_id")
    game = Game.query.get(game_id)
    game.is_end = 1

    day_id = session.get("day_id")
    day = Day.query.get(day_id)
    g.cash = day.cash
    g.other_value = day.total_value - g.cash
    g.loss = round(g.other_value/2,1)
    g.profit = g.cash + g.other_value - g.loss - 70000
    g.roe = round(g.profit/700,2)

    game.game_profit = g.profit
    db.session.commit()
    return render_template("end_by_close.html")
