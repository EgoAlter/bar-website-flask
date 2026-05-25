# The Mad House Newcastle — Flask Web App

A full-stack web application built as a practice replacement for an existing Squarespace site for a real cocktail bar in Newcastle, UK. Built as a portfolio and learning project using Python/Flask.

**Live site (original):** [themadhousenewcastle.co.uk](https://themadhousenewcastle.co.uk)

---

## What it does

A multi-page bar website with a password-protected admin interface for managing content. All menu data is stored in a SQLite database and served dynamically — no hardcoded content in templates.

**Public pages:**
- Homepage with hero, opening hours, happy hour info, and venue highlights
- Separate menu pages per venue (Pink Lane and Dean Street)
- Bottomless brunch page
- Private hire enquiry page
- Photo gallery (locally hosted images)
- Contact form with email delivery
- Gift cards page
- Booking page linking to external reservation system

**Admin interface (`/admin`):**
- Password-protected login
- Dashboard showing all menu items across both venues
- Add, edit, and delete menu items
- Toggle item availability (hide without deleting)

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Database | SQLite via Flask-SQLAlchemy |
| Templates | Jinja2 |
| Frontend | Bootstrap 5.3 (dark theme) |
| Email | Flask-Mail with Mailtrap (dev) |
| Auth | Flask session-based login |
| Environment | python-dotenv |
| Deployment | Cloudflare Tunnel |

---

## Project structure

```
myapp/
├── app.py              # Routes, models, application config
├── data.py             # Venue info (addresses, hours, booking URLs)
├── seed.py             # One-time database seeding script
├── requirements.txt
├── .env                # Not committed — see below
├── static/
│   ├── css/style.css
│   └── img/gallery/    # Locally hosted gallery images
└── templates/
    ├── layout.html     # Public site base template
    ├── index.html
    ├── menu_pink_lane.html
    ├── menu_dean_street.html
    ├── bottomless_brunch.html
    ├── private_hire.html
    ├── gallery.html
    ├── contact.html
    ├── gift_cards.html
    ├── book.html
    └── admin/
        ├── layout.html
        ├── login.html
        ├── dashboard.html
        ├── add.html
        └── edit.html
```

---

## Running locally

**1. Clone the repo**
```bash
git clone https://github.com/EgoAlter/madhouse-flask.git
cd madhouse-flask
```

**2. Create and activate a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create a `.env` file** in the project root:
```
MAIL_SERVER=sandbox.smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=your_mailtrap_username
MAIL_PASSWORD=your_mailtrap_password
MAIL_USE_TLS=True
MAIL_USE_SSL=False
ADMIN_PASSWORD=your_chosen_admin_password
```

**5. Seed the database**
```bash
python3 seed.py
```

**6. Run the app**
```bash
python3 app.py
```

Visit `http://localhost:5000`

---

## Key architectural decisions

**Single source of truth for venue data** — addresses, phone numbers, opening hours, and booking URLs all live in `data.py`. Changing a phone number updates every page simultaneously.

**Data-driven menus** — menu items are stored in SQLite with `venue`, `category`, `available`, `name`, `description`, and `price` fields. The public menu pages query the database and render only available items. Adding or hiding an item requires no code changes.

**Separate admin layout** — the admin interface uses its own base template (`admin/layout.html`) completely independent of the public site, so admin UI changes never affect the customer-facing pages.

**Environment separation** — all secrets (mail credentials, admin password) live in `.env` and are never committed. The seed script can be re-run safely — it clears and repopulates the database each time.

---

## What's next / planned features

- [ ] User registration and profiles (for loyalty programme)
- [ ] Pre-order system for bottomless brunch (replacing Google Forms)
- [ ] Image upload in admin (gallery management without filesystem access)
- [ ] Cloudinary integration for cloud-hosted images
- [ ] Migrate to PostgreSQL for production deployment
- [ ] Rebuild in Django as a learning exercise

---

## Background

This project was built as a practical learning exercise after completing CS50x, CS50P, and CS50W. The goal was to take a real business problem — an inflexible Squarespace site with inconsistent data and no easy way for the owner to manage content — and build a cleaner, more maintainable replacement from scratch.

It demonstrates server-side rendering with Flask/Jinja2, relational data modelling, form handling, session-based authentication, and the separation of data, logic, and presentation that makes a codebase maintainable at scale.
