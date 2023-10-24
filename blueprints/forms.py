import wtforms
from wtforms.validators import length,number_range

class AdminLoginForm(wtforms.Form):
    admin_name = wtforms.StringField(validators=[length(min=3,max=20)])
    admin_password = wtforms.StringField(validators=[length(min=3,max=20)])

class ClassCreateForm(wtforms.Form):
    class_name = wtforms.StringField(validators=[length(min=1,max=20)])
    class_password = wtforms.StringField(validators=[length(min=1,max=20)])
    confirm_class_password = wtforms.StringField(validators=[length(min=1,max=20)])
    class_type = wtforms.StringField()

class UserCreateForm(wtforms.Form):
    class_name = wtforms.StringField(validators=[length(min=1,max=20)])
    class_password = wtforms.StringField(validators=[length(min=1,max=20)])
    user_name = wtforms.StringField(validators=[length(min=1,max=20)])
    first_login_label = wtforms.StringField()

class PurchaseForm(wtforms.Form):
    bundle1 = wtforms.IntegerField(validators=[number_range(min=0,max=99,message='超出范围')])
    bundle2 = wtforms.IntegerField(validators=[number_range(min=0,max=99,message='超出范围')])
    bundle3 = wtforms.IntegerField(validators=[number_range(min=0,max=99,message='超出范围')])

class RecipeForm(wtforms.Form):
    lemon_per_cup = wtforms.IntegerField(validators=[number_range(min=0,max=99,message='超出范围')])
    sugar_per_cup = wtforms.IntegerField(validators=[number_range(min=0,max=99,message='超出范围')])
    ice_per_cup = wtforms.IntegerField(validators=[number_range(min=0,max=99,message='超出范围')])
    price_per_cup = wtforms.IntegerField(validators=[number_range(min=1,max=99,message='超出范围')])

class MessageForm(wtforms.Form):
    name = wtforms.StringField(validators=[length(min=1,max=200)])
    email = wtforms.StringField(validators=[length(min=1,max=200)])
    message = wtforms.StringField(validators=[length(min=1,max=10000)])
