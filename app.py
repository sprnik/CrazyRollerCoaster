from flask import Flask
from config import Config
from admin.orm.models import db, User
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = '9960ff2b1b05954d50a6de7f556174f1e2951054110fafb8'  # Используйте сгенерированный ключ

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    from routes.user import main as user_main
    from admin.orm.manage_orm import main as admin_orm_main
    from admin.sql.manage_sql import main as admin_sql_main
    from routes.attractions import initialize_attractions

    initialize_attractions()
    role = input("Are you an Admin or User? ").strip().lower()
    
    if role == "admin":
        orm_or_sql = input("Do you want to use ORM or SQL? ").strip().lower()
        if orm_or_sql == "orm":
            admin_orm_main()
        elif orm_or_sql == "sql":
            admin_sql_main()
        else:
            print("Invalid input.")
    elif role == "user":
        user_main()
    else:
        print("Invalid role.")
