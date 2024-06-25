from common.common_orm import *
from app import app
import sys

def main():
    print("Welcome, Admin!")
    while True:
        print("\n1. Add Visitor")
        print("2. List Visitors")
        print("3. Add Ticket")
        print("4. List Tickets")
        print("5. Update Visitor")
        print("6. Delete Visitor")
        print("7. Find Visitor")
        print("8. List Users with Password Hashes")
        print("9. Get Ticket Price")
        print("10. Start Visit")
        print("11. List Visits")
        print("12. End Visit")
        print("13. Exit")
        choice = input("Enter choice: ")

        with app.app_context():
            if choice == '1':
                name = input("Enter name: ")
                date_of_birth = input("Enter date of birth (YYYY-MM-DD): ")
                email = input("Enter email: ")
                print(add_visitor(name, date_of_birth, email))
            elif choice == '2':
                visitors = list_visitors()
                for visitor in visitors:
                    print(f"ID: {visitor.id}, Name: {visitor.name}, Date of Birth: {visitor.date_of_birth}, Email: {visitor.email}")
            elif choice == '3':
                visitor_id = input("Enter visitor ID: ")
                ticket_type = input("Enter ticket type (standard, VIP, Platinum): ")
                print(add_ticket(visitor_id, ticket_type))
            elif choice == '4':
                tickets = list_tickets()
                for ticket in tickets:
                    print(f"ID: {ticket.id}, Visitor ID: {ticket.visitor_id}, Type: {ticket.ticket_type}, Is Adult: {ticket.is_adult}, Purchase Date: {ticket.purchase_date}")
            elif choice == '5':
                visitor_id = input("Enter visitor ID to update: ")
                name = input("Enter new name: ")
                date_of_birth = input("Enter new date of birth (YYYY-MM-DD): ")
                email = input("Enter new email: ")
                print(update_visitor(visitor_id, name, date_of_birth, email))
            elif choice == '6':
                visitor_id = input("Enter visitor ID to delete: ")
                print(delete_visitor(visitor_id))
            elif choice == '7':
                name = input("Enter name to search: ")
                visitors = find_visitor(name)
                for visitor in visitors:
                    print(f"ID: {visitor.id}, Name: {visitor.name}, Date of Birth: {visitor.date_of_birth}, Email: {visitor.email}")
            elif choice == '8':
                users = list_users_with_password_hashes()
                for user in users:
                    print(f"ID: {user['id']}, Username: {user['username']}, Email: {user['email']}, Password Hash: {user['password_hash']}")
            elif choice == '9':
                ticket_type = input("Enter ticket type (standard, VIP, Platinum): ").lower()
                print(get_ticket_price(ticket_type))
            elif choice == '10':
                attractions = Attraction.query.all()
                for attraction in attractions:
                    print(f"ID: {attraction.id}, Name: {attraction.name}, Theme Group: {attraction.theme_group}, Duration: {attraction.duration}")
                visitor_id = input("Enter visitor ID: ")
                attraction_id = input("Enter attraction ID: ")
                print(start_visit(visitor_id, attraction_id))
            elif choice == '11':
                visits = list_visits()
                for visit in visits:
                    print(f"ID: {visit.id}, Visitor ID: {visit.visitor_id}, Attraction ID: {visit.attraction_id}, Start Time: {visit.visit_start_time}, End Time: {visit.visit_end_time}")
            elif choice == '12':
                visit_id = input("Enter visit ID to end: ")
                print(end_visit(visit_id))
            elif choice == '13':
                sys.exit()
            else:
                print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
