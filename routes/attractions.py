from admin.orm.models import db, Attraction
from app import app

def initialize_attractions():
    with app.app_context():
        if not Attraction.query.filter_by(name="Roller Coaster").first():
            db.session.add(Attraction(name="Roller Coaster", theme_group="extreme", duration=5))
        if not Attraction.query.filter_by(name="Ferris Wheel").first():
            db.session.add(Attraction(name="Ferris Wheel", theme_group="classic", duration=10))
        if not Attraction.query.filter_by(name="Haunted House").first():
            db.session.add(Attraction(name="Haunted House", theme_group="adventure", duration=15))
        db.session.commit()
