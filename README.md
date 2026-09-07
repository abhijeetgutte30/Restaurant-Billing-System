# Restaurant Billing System

A web-based restaurant management system built using Python and Flask.

This project was created to manage some of the basic day-to-day work of a restaurant from one place. It includes billing, menu management, customer records, inventory tracking and reports.

## Features

### Billing

* Create restaurant bills
* Add multiple menu items to a bill
* Calculate subtotal, GST, discount and final amount
* Select payment method
* Generate invoice numbers

### Menu Management

* Add new menu items
* Edit menu items
* Delete menu items
* Manage items by category
* Set item prices

### Customer Management

* Add customer details
* Store customer mobile number
* Store table number
* Connect customer details with bills

### Inventory

* Add daily stock
* Track opening stock
* Track stock added during the day
* Update current/remaining stock manually
* Carry forward remaining stock to the next day
* Low stock and out-of-stock indicators

### Reports

* View sales information
* Track orders
* Check daily revenue
* View payment-related information

### Admin Login

* Protected admin dashboard
* Login authentication
* Password hashing

## Tech Stack

**Backend**

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Login
* Flask-Bcrypt

**Frontend**

* HTML
* CSS
* JavaScript
* Font Awesome

**Database**

* SQLite
* PostgreSQL compatible setup for deployment

## Project Structure
RestaurantBillingSystem/
│
├── app.py
├── config.py
├── requirements.txt
├── database.db
│
├── database/
│   └── database.py
│
├── models/
│   └── models.py
│
├── routes/
│   ├── auth.py
│   ├── menu.py
│   ├── billing.py
│   ├── customers.py
│   └── inventory.py
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── menu.html
│   ├── billing.html
│   ├── customers.html
│   └── inventory.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── js/
        └── script.js

## Running the Project Locally

### 1. Clone the repository


git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git

### 2. Open the project folder


cd RestaurantBillingSystem


### 3. Create a virtual environment



### 4. Activate the virtual environment

**Windows:**


venv\Scripts\activate


### 5. Install the required packages


pip install -r requirements.txt


### 6. Run the application


python app.py


The application will start on the local Flask server.

## Database

The project currently uses SQLite for development.

The application is structured using SQLAlchemy, so the database configuration can be changed for a production database such as PostgreSQL when required.

## Security

Sensitive values such as the Flask secret key should be stored using environment variables instead of being committed directly to the repository.

## What I Learned

While building this project, I worked with:

* Flask application structure
* Routing and Blueprints
* SQLAlchemy models and relationships
* User authentication
* Password hashing
* CRUD operations
* Form handling
* Database management
* Frontend and backend integration
* Git and GitHub
* Deploying a Flask application

## Future Improvements

Some things I would like to add or improve in the future:

* Better invoice/receipt printing
* More detailed sales reports
* PostgreSQL production database
* Role-based access for staff
* Better inventory history
* Improved mobile responsiveness
* More dashboard analytics

## About the Developer

**Abhijeet Gutte**

B.Sc. IT student interested in Python, web development and backend development.

I built this project as a practical way to learn Flask and understand how a real-world business application is structured.

## License

This project is for learning and portfolio purposes.
