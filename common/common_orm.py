from datetime import datetime
from admin.orm.models import db, Visitor, Ticket, Attraction, Visit, User
from flask_login import login_user as flask_login_user, logout_user as flask_logout_user
from common.utils import is_adult, can_access_attraction

def list_users_with_password_hashes():
    users = User.query.all()
    return [{"id": user.id, "username": user.username, "email": user.email, "password_hash": user.password_hash} for user in users]

def add_visitor(name, date_of_birth_str, email):
    try:
        date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d')
        new_visitor = Visitor(
            name=name,
            date_of_birth=date_of_birth,
            email=email,
            is_adult=is_adult(date_of_birth)
        )
        db.session.add(new_visitor)
        db.session.commit()
        return "Visitor added successfully"
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}"

def list_visitors():
    visitors = Visitor.query.all()
    return visitors

def add_ticket(visitor_id, ticket_type):
    visitor = Visitor.query.get(visitor_id)
    if not visitor:
        return "Visitor not found"

    new_ticket = Ticket(
        visitor_id=visitor_id,
        ticket_type=ticket_type,
        is_adult=visitor.is_adult,
        purchase_date=datetime.now()
    )
    db.session.add(new_ticket)
    db.session.commit()
    return "Ticket added successfully"

def list_tickets():
    tickets = Ticket.query.all()
    return tickets


def update_visitor(visitor_id, name, date_of_birth_str, email):
    try:
        visitor = Visitor.query.get(visitor_id)
        if not visitor:
            return "Visitor not found"

        # Проверка на дублирование email
        existing_visitor = Visitor.query.filter(Visitor.email == email, Visitor.id != visitor_id).first()
        if existing_visitor:
            return "A visitor with this email already exists."

        visitor.name = name
        visitor.date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d')
        visitor.email = email
        visitor.is_adult = is_adult(visitor.date_of_birth)
        db.session.commit()
        return "Visitor updated successfully"
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}"

def delete_visitor(visitor_id):
    try:
        visitor = Visitor.query.get(visitor_id)
        if not visitor:
            return "Visitor not found"

        tickets = Ticket.query.filter_by(visitor_id=visitor_id).all()
        for ticket in tickets:
            db.session.delete(ticket)
        
        visits = Visit.query.filter_by(visitor_id=visitor_id).all()
        for visit in visits:
            db.session.delete(visit)

        user = User.query.filter_by(email=visitor.email).first()
        if user:
            db.session.delete(user)

        db.session.delete(visitor)
        db.session.commit()
        return "Visitor and related records deleted successfully"
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}"


def find_visitor(name):
    visitors = Visitor.query.filter(Visitor.name.ilike(f"%{name}%")).all()
    return visitors

def register_user(username, email, password, date_of_birth_str):
    try:
        # Проверка, существует ли пользователь с таким адресом электронной почты
        if User.query.filter_by(email=email).first():
            return "A user with this email already exists."

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        # Преобразование строки даты рождения в объект datetime
        date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d')
        
        # Создание записи в таблице Visitor
        new_visitor = Visitor(
            name=username,
            date_of_birth=date_of_birth,
            email=email,
            is_adult=is_adult(date_of_birth)
        )
        db.session.add(new_visitor)
        db.session.commit()

        return "User registered successfully"
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}"

def login_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return "Logged in successfully"
    else:
        return "Invalid email or password"

def logout_current_user():
    return "Logged out successfully"

def get_ticket_price(ticket_type):
    from admin.orm.strategy import TicketContext, StandardTicket, VIPTicket, PlatinumTicket
    
    if ticket_type == 'standard':
        context = TicketContext(StandardTicket())
    elif ticket_type == 'vip':
        context = TicketContext(VIPTicket())
    elif ticket_type == 'platinum':
        context = TicketContext(PlatinumTicket())
    else:
        return "Invalid ticket type"

    return f"The price for {ticket_type} ticket is {context.get_price()}"

def start_visit(visitor_id, attraction_id):
    visitor = Visitor.query.get(visitor_id)
    if not visitor:
        return "Visitor not found"
    
    ticket = Ticket.query.filter_by(visitor_id=visitor_id).order_by(Ticket.purchase_date.desc()).first()
    if not ticket:
        return "No valid ticket found for visitor"
    
    attraction = Attraction.query.get(attraction_id)
    if not attraction:
        return "Attraction not found"
    
    if not can_access_attraction(ticket.ticket_type, attraction.theme_group):
        return f"Access denied: {ticket.ticket_type} ticket does not allow access to {attraction.theme_group} attractions"

    new_visit = Visit(
        visitor_id=visitor_id,
        attraction_id=attraction_id,
        visit_start_time=datetime.now()
    )
    db.session.add(new_visit)
    db.session.commit()
    return "Visit started successfully"

def end_visit(visit_id):
    visit = Visit.query.get(visit_id)
    if not visit:
        return "Visit not found"
    
    visit.visit_end_time = datetime.now()
    db.session.commit()
    return "Visit ended successfully"

def list_visits():
    visits = Visit.query.all()
    return visits


