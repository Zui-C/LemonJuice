from exts import db
from datetime import datetime
class MessageTable(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    message = db.Column(db.String(10000),nullable=False)

class Admins(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    admin_name = db.Column(db.String(200), nullable=False, unique=True)
    admin_password = db.Column(db.String(200),nullable=False)
    def __repr__(self):
        return "<User(id='%s',admin_name='%s',admin_password='%s')>" % (self.id,self.admin_name,self.admin_password)

class Class(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    class_name = db.Column(db.String(200), nullable=False, unique=True)
    class_password = db.Column(db.String(200),nullable=False)
    class_student_number = db.Column(db.Integer,nullable=False,default=0)
    class_type = db.Column(db.String(200),nullable=False)
    end_day = db.Column(db.Integer,default=48)
    max_termination = db.Column(db.Integer,default=3)
    create_time = db.Column(db.DateTime,default=datetime.now)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(200), nullable=False)

    # user 当前的游戏次数和目前的游戏id
    game_number = db.Column(db.Integer,nullable=False,default=0)
    # current_game_id = db.Column(db.Integer,nullable=False,default=0)

    create_time = db.Column(db.DateTime,default=datetime.now)

    # 外键
    class_id = db.Column(db.Integer,db.ForeignKey("class.id"))
    belong_class = db.relationship("Class",backref="user")

class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)

    # 当前所进行到的游戏天数
    current_day_number = db.Column(db.Integer,nullable=False,default=0)
    # 当前用户的游戏的次数
    user_game_number = db.Column(db.Integer,nullable=False,default=0)
    game_profit = db.Column(db.Float)

    # 当前天数对应的Day id
    # current_day_id = db.Column(db.Integer,nullable=False,default=0)
    # 游戏是否结束
    is_end = db.Column(db.Boolean,nullable=False,default=0)

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    belong_user = db.relationship("User",backref="game")

class Day(db.Model):
    __tablename__ = 'day'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)

    # 当前游戏天数
    day_number = db.Column(db.Integer)

    # 温度和天气
    weather = db.Column(db.String(20))
    temperature = db.Column(db.DECIMAL(3,1))

    # 配方
    lemon_per_cup = db.Column(db.Integer)
    sugar_per_cup = db.Column(db.Integer)
    ice_per_cup = db.Column(db.Integer)
    price_per_cup = db.Column(db.Integer)

    # 原料购买
    purchase = db.Column(db.Text,default='')

    # 满意度
    satisfaction = db.Column(db.DECIMAL(5,4))
    popularity = db.Column(db.DECIMAL(5,4))
    purchase_people = db.Column(db.Integer)
    potential_people = db.Column(db.Integer)

    # 库存资源
    lemon = db.Column(db.Integer)
    sugar = db.Column(db.Integer)
    ice = db.Column(db.Integer)
    cup = db.Column(db.Integer)
    cash = db.Column(db.Integer)
    # 库存价值
    lemon_value = db.Column(db.Float)
    sugar_value = db.Column(db.Float)
    ice_value = db.Column(db.Float)
    cup_value = db.Column(db.Float)
    # 待摊装修费用
    fit_up_value = db.Column(db.Float)
    # 设备残值
    equipment_value = db.Column(db.Float)
    # 租金待摊
    rent_value = db.Column(db.Float)
    # 工资待摊
    wages_value = db.Column(db.Float)
    # 全部资产价值 包括现金
    total_value = db.Column(db.Float)

    # 经营成本
    lemon_cost = db.Column(db.Float)
    sugar_cost = db.Column(db.Float)
    ice_cost = db.Column(db.Float)
    cup_cost = db.Column(db.Float)
    rent_cost = db.Column(db.Integer)
    wages_cost = db.Column(db.Integer)
    equipment_cost = db.Column(db.Float)
    total_cost = db.Column(db.Float)

    # 营业费用 装修的折旧
    oper_cost = db.Column(db.Float)

    # 浪费的库存计费用 营业外支出
    lemon_waste = db.Column(db.Integer)
    lemon_waste_value = db.Column(db.Float)
    ice_waste = db.Column(db.Integer)
    ice_waste_value = db.Column(db.Float)
    total_waste_value = db.Column(db.Float)

    revenue = db.Column(db.Integer)
    revenue_sum = db.Column(db.Integer)
    profit = db.Column(db.Float)
    profit_sum = db.Column(db.Float)

    # 店面
    home_type = db.Column(db.Integer)
    home_pay_day = db.Column(db.Integer)

    # 外键
    game_id = db.Column(db.Integer,db.ForeignKey("game.id"))
    belong_game = db.relationship("Game",backref="day")