import math
import random
def simulate(home_type, recipe, resource, weather, temperature, last_popularity):
    if home_type == 1:
        base = 2500
    else:
        base = 8000
    lemon,sugar,ice,cup,cash = resource
    lemon_per_cup, sugar_per_cup, ice_per_cup, price_per_cup = recipe

    # 天气参数影响
    weather_dict = {'sunny': 1,'cloudy':0.75,'windy':0.65,'rainy':0.4,'thunder':0.25}
    fact_weather = weather_dict[weather]
    # 温度参数影响
    fact_temperature = math.sin((temperature-20)/80*math.pi)/2 + 1
    # 潜在顾客数量 受到 天气 温度 欢迎程度影响
    potential_people = base*fact_weather*fact_temperature*last_popularity
    potential_people = int(potential_people)

    # 配方与满意度
    fact_lemon = lemon_per_cup/5 if lemon_per_cup < 5 else 1
    fact_sugar = sugar_per_cup/4 if sugar_per_cup < 4 else 1
    if lemon_per_cup > sugar_per_cup:
        fact_l_s = sugar_per_cup/lemon_per_cup
    elif lemon_per_cup == sugar_per_cup and sugar_per_cup == 0:
        fact_l_s = 1
    else:
        fact_l_s = (lemon_per_cup/5)/(sugar_per_cup/4)
    # 配方影响为三者加权
    fact_taste = 0.8*fact_lemon + 0.15*fact_sugar + 0.05*fact_l_s

    # 温度与冰块数量
    # if 3*ice_per_cup > temperature:
    #     fact_ice = temperature/(3*ice_per_cup)
    # elif ice_per_cup == temperature and ice_per_cup == 0:
    #     fact_ice = 1
    # else:
    #     fact_ice = (3*ice_per_cup)/(temperature)

    fact_ice = 1 - abs((3*ice_per_cup-temperature+5)/20)
    if fact_ice < 0:
        fact_ice = 0
    # 满意程度 受到温度 与 配方影响
    fact_recipe = fact_taste*0.8+fact_ice*0.2


    # 满意程度还受到价格的影响
    if home_type == 3:
        if price_per_cup > 5:
            fact_price = 6/(price_per_cup-2)
        else:
            fact_price = 6/4
    else:
        if price_per_cup > 2:
            fact_price = 5/price_per_cup
        else:
            fact_price = 5/3

    satisfaction = fact_recipe * fact_price

    if satisfaction > 1:
        satisfaction = 1
    # 最终购买人数
    purchase_people = int(potential_people*satisfaction)

    # 判断够不够卖
    a = recipe[0:3] + [1]
    b = resource[0:4]
    c = list(map(lambda x, y: y/x-purchase_people if x else 0, a, b))
    index = c.index(min(c)) if min(c)< 0 else -1
    if index >= 0:
        # 记录供应参数
        fact_supply = (b[index]//a[index])/purchase_people
        purchase_people = b[index]//a[index]
        satisfaction = (b[index]/a[index])/potential_people
    else:
        fact_supply = 1
    # 更新资源
    resource[0:4] = list(map(lambda x, y: y-purchase_people*x, a, b))
    resource[4] = resource[4] + recipe[3]*purchase_people

    # 损失
    ice_waste = resource[2]
    resource[2] = 0
    lemon_waste = int(resource[0]*0.1)
    resource[0] = resource[0]-lemon_waste

    # 满意程度影响后续popularity
    popularity = last_popularity + (satisfaction-0.5)/12
    popularity = popularity if popularity > 0.02 else 0.01
    popularity = popularity if popularity < 0.99 else 0.99

    satisfaction = round(satisfaction,4)

    popularity = round(popularity,4)

    message_75_list = ['不错哦！']
    message_50_list = ['感觉还行。']
    message_supply_list = ['柠檬汁也能饥饿营销？']
    message_recipe_list = ['这味道不大对吧。']
    message_price_list = ['啧啧，这价格。']

    if satisfaction > 0.75:
        message = random.choice(message_75_list)
    elif 0.75 >= satisfaction > 0.5:
        message = random.choice(message_50_list)
    else:
        if fact_supply < 0.7:
            message = random.choice(message_supply_list)
        else:
            if fact_recipe > fact_price:
                message = random.choice(message_price_list)
            else:
                message = random.choice(message_recipe_list)

    return resource, purchase_people, potential_people, satisfaction, popularity,lemon_waste,ice_waste,message

def random_day(day):
    # 温度随机
    year_day = 48
    month_tem = [35,35,33,27,20,10,8,8,15,20,22,28]
    mon_day = year_day//12
    avg_tem = month_tem[(day%year_day)//mon_day]
    temperature = round(avg_tem + (random.random()-0.5)*10,1)
    # 天气随机
    weather_list = ['sunny','sunny','cloudy','cloudy','cloudy','windy','windy','windy','rainy','rainy','thunder']
    weather = random.choice(weather_list)
    return temperature, weather