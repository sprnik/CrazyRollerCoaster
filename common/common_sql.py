from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from common.utils import is_adult, can_access_attraction
from admin.orm.strategy import TicketContext, StandardTicket, VIPTicket, PlatinumTicket

def list_users_with_password_hashes():
    result = db.session.execute("SELECT id, username, email, password_hash FROM user")
    users = result.fetchall()
    return [{"id": user.id, "username": user.username, "email": user.email, "password_hash": user.password_hash} for user in users]

def add_visitor(name, date_of_birth_str, email):
    try:
        date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d')
        is_adult_flag = is_adult(date_of_birth)
        db.session.execute(f"INSERT INTO visitor (name, date_of_birth, email, is_adult) VALUES ('{name}', '{date_of_birth}', '{email}', {is_adult_flag})")
        db.session.commit()
        return "Visitor added successfully"
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}"

def list_visitors():
    result = db.session.execute("SELECT * FROM visitor")
    return result.fetchall()

def add_ticket(visitor_id, ticket_type):
    try:
        # Проверка наличия посетителя
        visitor = db.session.execute(f"SELECT * FROM visitor WHERE id = {visitor_id}").fetchone()
        if not visitor:
            return "Visitor not found"

        # Получение параметров посетителя
        is_adult_flag = visitor.is_adult
        purchase_date = datetime.now()
        price = get_ticket_price(ticket_type)

        # Добавление нового билета
        db.session.execute(
            f"INSERT INTO ticket (visitor_id, ticket_type, is_adult, purchase_date) VALUES "
            f"({visitor_id}, '{ticket_type}', {is_adult_flag}, '{purchase_date}')"
        )
        db.session.commit()
        return "Ticket added successfully"
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}"

def list_tickets():
    result = db.session.execute("SELECT * FROM ticket")
    return result.fetchall()

def update_visitor(visitor_id, name, date_of_birth_str, email):
    try:
        date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d')
        is_adult_flag = is_adult(date_of_birth)
        
        db.session.execute(
            f"UPDATE visitor SET name = '{name}', date_of_birth = '{date_of_birth}', email = '{email}', is_adult = {is_adult_flag} WHERE id = {visitor_id}"
        )
        db.session.commit()
        return "Visitor updated successfully"
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}"

def delete_visitor(visitor_id):
    try:
        visitor = db.session.execute(f"SELECT * FROM visitor WHERE id = {visitor_id}").fetchone()
        if not visitor:
            return "Visitor not found"

        db.session.execute(f"DELETE FROM ticket WHERE visitor_id = {visitor_id}")
        db.session.execute(f"DELETE FROM visit WHERE visitor_id = {visitor_id}")
        db.session.execute(f"DELETE FROM visitor WHERE id = {visitor_id}")

        user = db.session.execute(f"SELECT * FROM user WHERE email = '{visitor.email}'").fetchone()
        if user:
            db.session.execute(f"DELETE FROM user WHERE email = '{visitor.email}'")

        db.session.commit()
        return "Visitor and related records deleted successfully"
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}"

def find_visitor(name):
    result = db.session.execute(f"SELECT * FROM visitor WHERE name LIKE '%{name}%'")
    return result.fetchall()

def register_user(username, email, password, date_of_birth_str):
    try:
        existing_user = db.session.execute(f"SELECT * FROM user WHERE email = '{email}'").fetchone()
        if existing_user:
            return "A user with this email already exists."

        password_hash = generate_password_hash(password)
        db.session.execute(f"INSERT INTO user (username, email, password_hash) VALUES ('{username}', '{email}', '{password_hash}')")
        db.session.commit()

        add_visitor(username, date_of_birth_str, email)
        return "User registered successfully"
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}"

def login_user(email, password):
    user = db.session.execute(f"SELECT * FROM user WHERE email = '{email}'").fetchone()
    if user and check_password_hash(user.password_hash, password):
        return "Logged in successfully"
    else:
        return "Invalid email or password"

def logout_current_user():
    return "Logged out successfully"

def get_ticket_price(ticket_type):
    if ticket_type.lower() == 'standard':
        context = TicketContext(StandardTicket())
    elif ticket_type.lower() == 'vip':
        context = TicketContext(VIPTicket())
    elif ticket_type.lower() == 'platinum':
        context = TicketContext(PlatinumTicket())
    else:
        raise ValueError("Invalid ticket type")

    return context.get_price()

def start_visit(visitor_id, attraction_id):
    try:
        visitor = db.session.execute(f"SELECT * FROM visitor WHERE id = {visitor_id}").fetchone()
        if not visitor:
            return "Visitor not found"

        ticket = db.session.execute(f"SELECT * FROM ticket WHERE visitor_id = {visitor_id} ORDER BY purchase_date DESC").fetchone()
        if not ticket:
            return "No valid ticket found for visitor"

        attraction = db.session.execute(f"SELECT * FROM attraction WHERE id = {attraction_id}").fetchone()
        if not attraction:
            return "Attraction not found"

        if not can_access_attraction(ticket.ticket_type, attraction.theme_group):
            return f"Access denied: {ticket.ticket_type} ticket does not allow access to {attraction.theme_group} attractions"

        db.session.execute(
            f"INSERT INTO visit (visitor_id, attraction_id, visit_start_time) VALUES ({visitor_id}, {attraction_id}, '{datetime.now()}')"
        )
        db.session.commit()
        return "Visit started successfully"
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}"

def end_visit(visit_id):
    try:
        visit = db.session.execute(f"SELECT * FROM visit WHERE id = {visit_id}").fetchone()
        if not visit:
            return "Visit not found"

        db.session.execute(f"UPDATE visit SET visit_end_time = '{datetime.now()}' WHERE id = {visit_id}")
        db.session.commit()
        return "Visit ended successfully"
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}"


def list_visits():
    result = db.session.execute("SELECT * FROM visit")
    return result.fetchall()
