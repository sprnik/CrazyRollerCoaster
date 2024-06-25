from common.common_orm import register_user as register_user_orm, login_user as login_user_orm, logout_current_user as logout_user_orm, add_ticket as add_ticket_orm, update_visitor as update_visitor_orm, start_visit as start_visit_orm
from common.common_sql import register_user as register_user_sql, login_user as login_user_sql, logout_current_user as logout_user_sql, add_ticket as add_ticket_sql, update_visitor as update_visitor_sql, start_visit as start_visit_sql
from flask_login import UserMixin
from admin.orm.models import User, Visitor, Attraction
from app import app, db
import sys

class MockCurrentUser(UserMixin):
    def __init__(self, user_id, email):
        self.id = user_id
        self.email = email

current_user = None

def main():
    global current_user
    print("Welcome, User!")
    orm_or_sql = input("Do you want to use ORM or SQL? ").strip().lower()

    if orm_or_sql == "orm":
        register_user = register_user_orm
        login_user = login_user_orm
        logout_user = logout_user_orm
        add_ticket = add_ticket_orm
        update_visitor = update_visitor_orm
        start_visit = start_visit_orm
    elif orm_or_sql == "sql":
        register_user = register_user_sql
        login_user = login_user_sql
        logout_user = logout_user_sql
        add_ticket = add_ticket_sql
        update_visitor = update_visitor_sql
        start_visit = start_visit_sql
    else:
        print("Invalid input.")
        return

    while True:
        if current_user:
            print("\n1. Buy Ticket")
            print("2. Update Profile")
            print("3. Start Visit")
            print("4. Logout")
            print("5. Exit")
        else:
            print("\n1. Register")
            print("2. Login")
            print("3. Exit")

        choice = input("Enter choice: ")

        with app.app_context():
            if current_user:
                visitor = Visitor.query.filter_by(email=current_user.email).first() if orm_or_sql == "orm" else db.session.execute(f"SELECT * FROM visitor WHERE email = '{current_user.email}'").fetchone()
                if choice == '1':
                    ticket_type = input("Enter ticket type (standard, VIP, Platinum): ")
                    print(add_ticket(visitor.id, ticket_type))
                elif choice == '2':
                    name = input("Enter new name: ")
                    date_of_birth = input("Enter new date of birth (YYYY-MM-DD): ")
                    email = input("Enter new email: ")
                    print(update_visitor(visitor.id, name, date_of_birth, email))
                elif choice == '3':
                    if orm_or_sql == "orm":
                        attractions = Attraction.query.all()
                    else:
                        attractions = db.session.execute("SELECT * FROM attraction").fetchall()
                    for attraction in attractions:
                        print(f"ID: {attraction.id}, Name: {attraction.name}, Theme Group: {attraction.theme_group}, Duration: {attraction.duration}")
                    attraction_id = input("Enter attraction ID: ")
                    print(start_visit(visitor.id, attraction_id))
                elif choice == '4':
                    print(logout_user())
                    current_user = None
                elif choice == '5':
                    sys.exit()
                else:
                    print("Invalid choice. Please try again.")
            else:
                if choice == '1':
                    username = input("Enter username: ")
                    email = input("Enter email: ")
                    password = input("Enter password: ")
                    date_of_birth = input("Enter date of birth (YYYY-MM-DD): ")
                    print(register_user(username, email, password, date_of_birth))
                elif choice == '2':
                    email = input("Enter email: ")
                    password = input("Enter password: ")
                    login_message = login_user(email, password)
                    print(login_message)
                    if "Logged in successfully" in login_message:
                        user = User.query.filter_by(email=email).first() if orm_or_sql == "orm" else db.session.execute(f"SELECT * FROM user WHERE email = '{email}'").fetchone()
                        current_user = MockCurrentUser(user.id, email)
                elif choice == '3':
                    sys.exit()
                else:
                    print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()