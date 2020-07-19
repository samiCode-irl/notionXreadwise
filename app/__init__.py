from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nwwgtomfbspmhn:8dd03519fee4577a84867bbeb159dc5cf29dc31e327bede7a8344da04c1bf733@ec2-52-22-216-69.compute-1.amazonaws.com:5432/dabgen2a0p9bdp'

app.config['SECRET_KEY'] = 'Super Secret Key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from app import routes
