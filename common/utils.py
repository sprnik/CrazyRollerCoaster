from datetime import datetime

def calculate_age(date_of_birth):
    today = datetime.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    return age

def is_adult(date_of_birth):
    age = calculate_age(date_of_birth)
    return age >= 18

def can_access_attraction(ticket_type, theme_group):
    if ticket_type == 'standard' and theme_group == 'classic':
        return True
    elif ticket_type == 'VIP' and theme_group in ['classic', 'adventure']:
        return True
    elif ticket_type == 'Platinum':
        return True
    return False
