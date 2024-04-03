from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
# PAssword Hash
from werkzeug.security import generate_password_hash
# File Admin
from flask_admin.contrib.fileadmin import FileAdmin
from os.path import dirname, join
# Vue personnalisee:
from flask_admin import BaseView, expose


app = Flask(__name__)
app.config.from_pyfile("./config.py")
app.app_context().push()
# 
db = SQLAlchemy(app)
# 
admin = Admin(app,template_mode="bootstrap3")

# MODELS
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    sexe = db.Column(db.Enum("Male","Female"), default="Female")
    birthday = db.Column(db.DateTime)
    # articles = db.relationship("Article",back_populates="user")
    def __repr__(self) -> str:
        return "{} {}".format(self.firstname,self.lastname)
    
class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # user = db.relationship("User",back_populates="article")
    user = db.relationship("User",backref="articles")

class UserView(ModelView):
    # column_exclude_list = ["password"]
    column_display_pk = True
    column_sortable_list = ('firstname', 'sexe')
    can_create = True
    can_edit = True
    can_delete = True
    can_export = True
    # 
    def on_model_change(self, form, model, is_created):
        passwordHashed = generate_password_hash(model.password,method="pbkdf2:sha256")
        model.password = passwordHashed
    #
    def is_accessible(self):
        # Ici, on met la logique 
        return False
    
    def inaccessible_callback(self, name, **kwargs):
        return "<h1>Degazzzz de la, il faut se connecter!</h1>"

class ArticleView(ModelView):
    form_columns =["title","description","user"]
    create_modal = True
    page_size = 2


class CommandesView(BaseView):
    @expose('/')
    def index(self):
        # ...des requetes, de la logique ici
        return self.render('admin/commande.html',commandes=["banane","coco","riz"])

# Ajout de modelView
# admin.add_view(ModelView(User,db.session))
admin.add_view(UserView(User,db.session))
admin.add_view(ArticleView(Article,db.session))

# 
upload_path = join(dirname(__file__),"uploads")
admin.add_view(FileAdmin(upload_path,'/uploads/',name="Uploads"))
#
admin.add_view(CommandesView(name="Commandes",endpoint="commandes"))


db.create_all()

if __name__ == "__main__":
    app.run()