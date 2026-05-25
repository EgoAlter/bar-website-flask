from app import app, db, MenuItem
from data import menu

with app.app_context():
    db.create_all()

    # Clear existing data so we can re-run safely
    MenuItem.query.delete()

    for venue_key, categories in menu.items():
        for category, items in categories.items():
            for item in items:
                entry = MenuItem(
                    name=item['name'],
                    description=item['description'],
                    price=item['price'],
                    category=category,
                    venue=venue_key
                )
                db.session.add(entry)

    db.session.commit()
    print(f"Database seeded successfully.")
    print(f"Total items: {MenuItem.query.count()}")