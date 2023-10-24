# 柠檬
lp1,lp2,lp3 = 640,3000,14330
ln1, ln2, ln3 = 1000, 5000, 25000
# 糖
sp1, sp2, sp3 = 250, 1000, 4150
sn1, sn2, sn3 = 1000, 5000, 25000
# 冰
ip1, ip2, ip3 = 50, 220, 1000
in1, in2, in3 = 5000, 25000, 125000
# 杯
cp1, cp2, cp3 = 500, 2250, 10000
cn1, cn2, cn3 = 1000, 5000, 25000
def buy_lemon(resource,bundles):
    # 购买数量
    b1,b2,b3 = bundles
    lemon = resource[0]
    cash = resource[4]
    pay = lp1*b1+lp2*b2+lp3*b3
    if cash < pay:
        return False
    else:
        resource[0] = lemon + ln1*b1 + ln2*b2 + ln3*b3
        resource[4] = round(cash - pay,0)
        return resource
def buy_sugar(resource,bundles):
    # 购买数量
    b1,b2,b3 = bundles
    sugar = resource[1]
    cash = resource[4]
    pay = sp1*b1+sp2*b2+sp3*b3
    if cash < pay:
        return False
    else:
        resource[1] = sugar + sn1*b1 + sn2*b2 + sn3*b3
        resource[4] = round(cash - pay,0)
        return resource
def buy_ice(resource,bundles):
    # 购买数量
    b1,b2,b3 = bundles
    ice = resource[2]
    cash = resource[4]
    pay = ip1*b1+ip2*b2+ip3*b3
    if cash < pay:
        return False
    else:
        resource[2] = ice + in1*b1 + in2*b2 + in3*b3
        resource[4] = round(cash - pay,0)
        return resource
def buy_cup(resource,bundles):
    # 购买数量
    b1,b2,b3 = bundles
    cup = resource[3]
    cash = resource[4]
    pay = cp1*b1+cp2*b2+cp3*b3
    if cash < pay:
        return False
    else:
        resource[3] = cup + cn1*b1 + cn2*b2 + cn3*b3
        resource[4] = round(cash - pay,0)
        return resource

def cal_cost(recipe):
    cost = recipe[0]*lp3/ln3+recipe[1]*sp3/sn3+recipe[2]*ip3/in3+cp3/cn3
    return round(cost,2)

def analyse_daily_purchase(s):
    l1,l2,s1,s2,i1,i2,c1,c2 = 0,0,0,0,0,0,0,0
    for i in s.split('-'):
        if 'l' in i:
            a = i[2:-1].split(',')
            b = [ln1,ln2,ln3]
            c = [lp1,lp2,lp3]
            l1 += sum(list(map(lambda e, f: int(e) * f, a, b)))
            l2 += sum(list(map(lambda e, f: int(e) * f, a, c)))
        elif 's' in i:
            a = i[2:-1].split(',')
            b = [sn1, sn2, sn3]
            c = [sp1, sp2, sp3]
            s1 += sum(list(map(lambda e, f: int(e) * f, a, b)))
            s2 += sum(list(map(lambda e, f: int(e) * f, a, c)))
        elif 'i' in i:
            a = i[2:-1].split(',')
            b = [in1, in2, in3]
            c = [ip1, ip2, ip3]
            i1 += sum(list(map(lambda e, f: int(e) * f, a, b)))
            i2 += sum(list(map(lambda e, f: int(e) * f, a, c)))
        elif 'c' in i:
            a = i[2:-1].split(',')
            b = [cn1, cn2, cn3]
            c = [cp1, cp2, cp3]
            c1 += sum(list(map(lambda e, f: int(e) * f, a, b)))
            c2 += sum(list(map(lambda e, f: int(e) * f, a, c)))
        else:
            pass
    total = l2 + s2 + i2 + c2
    return [l1,l2,s1,s2,i1,i2,c1,c2,total]

def max_supply(recipe,resource):
    recipe[3] = 1
    new_recipe = []
    new_resource = []
    for i in range(len(recipe)):
        if recipe[i] != 0:
            new_recipe.append(recipe[i])
            new_resource.append(resource[i])
    max_supply_people = min([new_resource[i]//new_recipe[i] for i in range(len(new_recipe))])
    return max_supply_people

def weather_trans(weather):
    dict = {'sunny': '晴', 'cloudy': '多云', 'windy': '阴', 'rainy': '雨', 'thunder': '闪电'}
    return dict.get(weather)