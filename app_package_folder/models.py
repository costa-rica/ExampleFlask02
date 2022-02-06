from app_package_folder import db, login_manager
from flask_login import UserMixin

from flask_script import Manager

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
    

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.id}','{self.email}','{self.password}')"