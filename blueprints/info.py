from flask import Blueprint, render_template, session,g,redirect,url_for,flash
from decorators import user_login_required
from models import Day, Game, User
from exts import db
import json
from game import utils

bp = Blueprint("info", __name__, url_prefix='/info')

@bp.route("/report_decision")
@user_login_required
def report_decision():
    day_number = session.get("day_number")
    if day_number < 2:
        flash("报表还未生成！")
        return redirect(url_for("play.start"))
    # 查询当前进行的游戏
    game_id = session.get("game_id")
    # 获得进行游戏每一天的数据
    days = Day.query.filter_by(game_id=game_id).order_by(Day.day_number).all()
    d = [{
        "c1": str(day.day_number),
        "c2": str(utils.weather_trans((day.weather))),
        "c3": str(day.temperature),
        "c4": str(day.lemon_per_cup),
        "c5": str(day.sugar_per_cup),
        "c6": str(day.ice_per_cup),
        "c7": str(day.price_per_cup),
        "c8": str(day.purchase_people),
        "c9": str(day.satisfaction),
        "c10": str(day.popularity)
    }
            for day in days][1:-1]

    data = json.dumps(d, separators=(',', ':'))
    return render_template('report_decision.html', data=data)



@bp.route("/report_profit")
@user_login_required
def report_profit():
    day_number = session.get("day_number")
    if day_number < 2:
        flash("报表还未生成！")
        return redirect(url_for("play.start"))
    # 查询当前进行的游戏
    game_id = session.get("game_id")
    # 获得进行游戏每一天的数据
    days = Day.query.filter_by(game_id=game_id).order_by(Day.day_number).all()
    d = [{
        "c1": str(day.day_number),
        "c2": str(day.lemon_cost),
        "c3": str(day.sugar_cost),
        "c4": str(day.ice_cost),
        "c5": str(day.cup_cost),
        "c6": str(day.total_cost),
        "c7": str(day.revenue),
        "c8": str(day.profit),
        "c9": str(day.profit_sum),
        "c10": str(day.total_waste_value),
        "c11": str(day.oper_cost),
        "c12": str(day.rent_cost),
        "c13": str(day.wages_cost),
        "c14": str(day.equipment_cost)
    }
            for day in days][1:-1]

    data = json.dumps(d, separators=(',', ':'))
    return render_template('report_profit.html', data=data)



@bp.route("/report_balance")
@user_login_required
def report_balance():
    day_number = session.get("day_number")
    if day_number < 2:
        flash("报表还未生成！")
        return redirect(url_for("play.start"))
    # 查询当前进行的游戏
    game_id = session.get("game_id")
    # 获得进行游戏每一天的数据
    days = Day.query.filter_by(game_id=game_id).order_by(Day.day_number).all()
    d = [{
        "c1": str(day.day_number),
        "c2": str(day.lemon),
        "c3": str(day.lemon_value),
        "c4": str(day.sugar),
        "c5": str(day.sugar_value),
        "c6": str(day.ice),
        "c7": str(day.ice_value),
        "c8": str(day.cup),
        "c9": str(day.cup_value),
        "c10": str(day.cash),
        "c11": str(day.total_value),
        "c12": str(day.total_value),
        "c13": str(day.wages_value),
        "c14": str(day.rent_value),
        "c15": str(day.fit_up_value),
        "c16": str(day.equipment_value)
    }
            for day in days][:-1]

    data = json.dumps(d, separators=(',', ':'))
    return render_template('report_balance.html', data=data)

@bp.route("/report_cashflow")
@user_login_required
def report_cashflow():
    day_number = session.get("day_number")
    if day_number < 2:
        flash("报表还未生成！")
        return redirect(url_for("play.start"))
    # 查询当前进行的游戏
    game_id = session.get("game_id")
    # 获得进行游戏每一天的数据
    days = Day.query.filter_by(game_id=game_id).order_by(Day.day_number).all()
    data = [{"c1":0,"c2":0,"c3":0,"c4":0,"c5":0,"c6":70000,"c7":70000,"c8":0,"c9":70000,"c10":0,"c11":0,"c12":0}]

    day = days[1]
    data_item = {}
    data_item["c1"] = str(day.day_number)
    data_item["c2"] = day.revenue
    data_item["c2"] = round(data_item["c2"],1)

    data_item["c3"] = day.lemon+day.sugar+day.ice+day.cup+day.lemon_value+day.sugar_value+ day.ice_value+ day.cup_value + day.total_waste_value
    data_item["c3"] = round(data_item["c3"],1)

    data_item["c4"] = day.wages_cost+day.wages_value
    data_item["c4"] = round(data_item["c4"],1)

    data_item["c5"] = day.rent_value+day.rent_cost
    data_item["c5"] = round(data_item["c5"],1)

    data_item["c6"] = day.fit_up_value+day.oper_cost
    data_item["c6"] = round(data_item["c6"],1)

    data_item["c7"] = data_item["c2"] - data_item["c3"] - data_item["c4"] - data_item["c5"] - data_item["c6"]
    data_item["c7"] = round(data_item["c7"],1)

    data_item["c8"] = -(day.equipment_value+day.equipment_cost)
    data_item["c8"] = round(data_item["c8"],1)

    data_item["c9"] = 0

    data_item["c10"] = data_item["c7"]+data_item["c8"]+data_item["c9"]
    data_item["c10"] = round(data_item["c10"],1)

    data_item["c11"] = day.cash-data_item["c10"]
    data_item["c11"] = round(data_item["c11"],1)

    data_item["c12"] = day.cash
    data_item["c12"] = round(data_item["c12"],1)

    data.append(data_item)

    data = json.dumps(data, separators=(',', ':'))
    return render_template('report_cashflow.html', data=data)

@bp.route("/report_sum_tables")
@user_login_required
def report_sum_tables():
    day_number = session.get("day_number")
    if day_number < 2:
        flash("报表还未生成！")
        return redirect(url_for("play.start"))
    # 查询当前进行的游戏
    game_id = session.get("game_id")
    # 获得进行游戏每一天的数据
    days = Day.query.filter_by(game_id=game_id).order_by(Day.day_number).all()
    sum_revenue = 0
    sum_lemon = 0
    sum_sugar = 0
    sum_ice = 0
    sum_cup = 0
    sum_wages_cost = 0
    sum_rent_cost = 0
    sum_equipment_cost = 0
    sum_oper_cost = 0
    sum_total_waste_value = 0
    sum_profit = 0

    # 营业外支出
    sum_waste = 0
    for day in days[1:-1]:
        sum_revenue += day.revenue
        sum_lemon += day.lemon_cost
        sum_sugar += day.sugar_cost
        sum_ice += day.ice_cost
        sum_cup += day.cup_cost
        sum_rent_cost += day.rent_cost
        sum_wages_cost += day.wages_cost
        sum_equipment_cost += day.equipment_cost
        sum_oper_cost += day.oper_cost
        sum_total_waste_value += day.total_waste_value

        sum_profit += day.profit
        sum_waste += day.total_waste_value


    # 利润表
    g.sum_revenue = sum_revenue
    g.sum_lemon = sum_lemon
    g.sum_sugar = sum_sugar
    g.sum_ice = sum_ice
    g.sum_cup = sum_cup
    g.sum_rent_cost = sum_rent_cost
    g.sum_wages_cost = sum_wages_cost
    g.sum_equipment_cost = sum_equipment_cost
    g.sum_total_cost = sum_lemon + sum_sugar + sum_ice + sum_cup + sum_rent_cost + sum_wages_cost +sum_equipment_cost
    g.sum_oper_cost = sum_oper_cost
    g.sum_total_waste_value = sum_total_waste_value
    g.sum_profit = sum_profit

    # 资产负债表
    day = days[-2]
    g.cash = day.cash
    g.lemon_value = day.lemon_value
    g.sugar_value = day.sugar_value
    g.ice_value = day.ice_value
    g.cup_value = day.cup_value
    g.sum_things = g.lemon_value + g.sugar_value + g.ice_value + g.cup_value

    g.wages_value = day.wages_value
    g.rent_value = day.rent_value
    g.fit_up_value = day.fit_up_value
    g.sum_things2 = g.wages_value + g.rent_value + g.fit_up_value
    g.equipment_value = day.equipment_value
    g.total_value = day.total_value


    # 现金流量表
    g.things_cash = g.sum_lemon + g.sum_sugar +g.sum_ice + g.sum_cup + g.lemon_value + g.sugar_value + g.ice_value + g.cup_value + g.sum_total_waste_value

    g.wage_cash = g.wages_value + g.sum_wages_cost
    g.rent_cash = g.rent_value + g.sum_rent_cost
    g.fit_up_cash = g.sum_oper_cost + g.fit_up_value

    g.sum_cash1 = g.sum_revenue - g.things_cash - g.wage_cash - g.rent_cash - g.fit_up_cash

    g.equipment_cash = g.equipment_value + g.sum_equipment_cost

    g.sum_cash2 = g.sum_cash1 - g.equipment_cash


    return render_template('report_sum_tables.html')