# CodeAlpha_EcommerceStore

A simple full-stack e-commerce website built for the **CodeAlpha Full Stack Development Internship (Task 1)**.

## Features
- Product listing with search
- Product details page
- Shopping cart (add, update quantity, remove) stored in the session
- User registration, login and logout
- Checkout and order processing (stock is reduced, order history is saved)
- Admin panel to manage products and orders

## Tech Stack
- Frontend: HTML, CSS, JavaScript (Django templates)
- Backend: Python, Django
- Database: SQLite

## Setup
```bash
python -m venv venv
venv\Scripts\activate        # Windows  (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
python manage.py makemigrations shop
python manage.py migrate
python manage.py seed                # adds sample products
python manage.py createsuperuser     # optional, for /admin
python manage.py runserver
```
Open http://127.0.0.1:8000/

## Project Structure
- `store_project/` – project settings and root URLs
- `shop/models.py` – Product, Order, OrderItem
- `shop/views.py` – catalogue, cart, checkout, auth views
- `shop/templates/` – HTML templates
