from flask import Flask,session,g,render_template,request,flash
from exts import db
from blueprints import play_bp, user_bp, admin_bp, info_bp, purchase_bp,recipe_bp,home_bp
from flask_migrate import Migrate
from models import Admins,Class,User,MessageTable
import config
from blueprints.forms import MessageForm

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# 数据库迁移
migrate = Migrate(app,db)

app.register_blueprint(play_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(info_bp)
app.register_blueprint(purchase_bp)
app.register_blueprint(recipe_bp)
app.register_blueprint(home_bp)


@app.route("/intro",methods=['GET','POST'])
def intro():
    return render_template("intro.html")

@app.route("/",methods=['GET','POST'])
def egate():
    if request.method == 'GET':
        return render_template("egate.html")
    else:
        form = MessageForm(request.form)
        if form.validate():
            name = form.name.data
            email = form.email.data
            message = form.message.data
            new_message = MessageTable(name=name, email=email, message=message)
            db.session.add(new_message)
            db.session.commit()
            flash('谢谢您的反馈！')
        else:
            flash('请正确填写信息！')
    return render_template("egate.html")


# 请求 -> before_request -> 视图函数 -> 视图函数返回模版 -> context_processor
@app.before_request
def before_request():
    admin_id = session.get("admin_id")
    user_id = session.get("user_id")
    if user_id:
        try:
            user = User.query.get(user_id)
            g.user = user.user_name
        except:
            pass
    if admin_id:
        try:
            admin = Admins.query.get(admin_id)
            g.admin = admin.admin_name
        except:
            pass
    app_resource = session.get("resource")
    if app_resource:
        g.resource = app_resource
    total_value = session.get("total_value")
    if total_value:
        g.total_value = total_value
    day_number = session.get("day_number")
    if day_number:
        g.day_number = day_number

@app.context_processor
def context_processor():
    data = {}
    if hasattr(g,"user"):
        data["user"] = g.user
    if hasattr(g,"admin"):
        data["admin"] = g.admin
    return data

if __name__ == '__main__':
    app.run('0.0.0.0',port=2222, debug=True)
