from flask import Flask, render_template
from datetime import datetime
from flask_login import login_required

from config import Config, bcrypt, login_manager
from database.database import db

from routes.auth import auth
from routes.menu import menu
from routes.billing import billing
from routes.customers import customers

from models.models import Admin, Menu, Customer, Bill, Inventory
from routes.inventory import inventory

app = Flask(__name__)

app.config.from_object(Config)


# =========================================================
# INITIALIZE EXTENSIONS
# =========================================================

db.init_app(app)

bcrypt.init_app(app)

login_manager.init_app(app)


# =========================================================
# REGISTER BLUEPRINTS
# =========================================================

app.register_blueprint(auth)

app.register_blueprint(menu)

app.register_blueprint(billing)

app.register_blueprint(customers)
app.register_blueprint(inventory)

# =========================================================
# CREATE DATABASE & DEFAULT ADMIN
# =========================================================

with app.app_context():

    db.create_all()

    admin = Admin.query.filter_by(
        username="admin"
    ).first()

    if admin is None:

        admin = Admin(
            username="admin"
        )

        admin.set_password(
            "admin123"
        )

        db.session.add(admin)

        db.session.commit()

        print("Default Admin Created")


# =========================================================
# PREMIUM HOME PAGE
# =========================================================

@app.route("/")
def home():

    return """
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>
        Restaurant Billing System | Abhijeet Gutte
    </title>


    <style>

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }


        html {
            scroll-behavior: smooth;
        }


        body {

            font-family:
                Arial,
                Helvetica,
                sans-serif;

            background: #0b0b0d;

            color: white;

            overflow-x: hidden;
        }


        /* ================= NAVBAR ================= */

        nav {

            position: fixed;

            top: 0;
            left: 0;

            width: 100%;
            height: 76px;

            display: flex;

            align-items: center;

            justify-content: space-between;

            padding: 0 7%;

            background:
                rgba(10, 10, 12, 0.75);

            backdrop-filter:
                blur(18px);

            border-bottom:
                1px solid rgba(255,255,255,0.08);

            z-index: 1000;
        }


        .logo {

            font-size: 22px;

            font-weight: 800;

            letter-spacing: 1px;
        }


        .logo span {

            color: #f5a623;
        }


        .nav-links {

            display: flex;

            align-items: center;

            gap: 30px;
        }


        .nav-links a {

            color: #ddd;

            text-decoration: none;

            font-size: 14px;

            transition: 0.3s;
        }


        .nav-links a:hover {

            color: #f5a623;
        }


        .nav-login {

            padding:
                11px 23px;

            border-radius:
                30px;

            background:
                #f5a623;

            color:
                #111 !important;

            font-weight:
                700;
        }


        .nav-login:hover {

            background:
                #ffc45c;

            transform:
                translateY(-2px);
        }


        /* ================= HERO ================= */

        .hero {

            min-height:
                100vh;

            display:
                flex;

            align-items:
                center;

            padding:
                120px 7% 70px;

            position:
                relative;

            overflow:
                hidden;

            background:

                radial-gradient(
                    circle at 75% 45%,
                    rgba(245,166,35,0.18),
                    transparent 30%
                ),

                radial-gradient(
                    circle at 90% 10%,
                    rgba(180,60,40,0.14),
                    transparent 30%
                ),

                #0b0b0d;
        }


        .hero-content {

            width: 55%;

            position:
                relative;

            z-index: 3;
        }


        .badge {

            display:
                inline-block;

            padding:
                8px 16px;

            border-radius:
                30px;

            background:
                rgba(245,166,35,0.10);

            border:
                1px solid
                rgba(245,166,35,0.35);

            color:
                #f5a623;

            font-size:
                13px;

            font-weight:
                600;

            margin-bottom:
                22px;
        }


        .hero h1 {

            font-size:
                clamp(48px, 6vw, 82px);

            line-height:
                1.03;

            letter-spacing:
                -3px;

            margin-bottom:
                25px;
        }


        .hero h1 span {

            color:
                #f5a623;
        }


        .hero p {

            color:
                #a7a7ad;

            font-size:
                18px;

            line-height:
                1.7;

            max-width:
                600px;

            margin-bottom:
                35px;
        }


        .hero-buttons {

            display:
                flex;

            gap:
                15px;

            flex-wrap:
                wrap;
        }


        .primary-btn {

            display:
                inline-block;

            padding:
                15px 30px;

            border-radius:
                10px;

            background:
                #f5a623;

            color:
                #111;

            text-decoration:
                none;

            font-weight:
                800;

            transition:
                0.3s;

            box-shadow:
                0 10px 30px
                rgba(245,166,35,0.18);
        }


        .primary-btn:hover {

            transform:
                translateY(-4px);

            background:
                #ffc45c;
        }


        .secondary-btn {

            display:
                inline-block;

            padding:
                15px 30px;

            border-radius:
                10px;

            border:
                1px solid
                rgba(255,255,255,0.15);

            color:
                white;

            text-decoration:
                none;

            font-weight:
                600;

            transition:
                0.3s;
        }


        .secondary-btn:hover {

            background:
                rgba(255,255,255,0.06);

            transform:
                translateY(-4px);
        }


        /* ================= HERO VISUAL ================= */

        .hero-visual {

            position:
                absolute;

            right:
                4%;

            top:
                18%;

            width:
                40%;

            height:
                65%;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;
        }


        .restaurant-card {

            width:
                440px;

            max-width:
                90%;

            height:
                500px;

            border-radius:
                28px;

            position:
                relative;

            overflow:
                hidden;

            background:

                linear-gradient(
                    145deg,
                    rgba(255,255,255,0.10),
                    rgba(255,255,255,0.025)
                );

            border:
                1px solid
                rgba(255,255,255,0.12);

            box-shadow:

                0 40px 100px
                rgba(0,0,0,0.55),

                inset 0 1px 0
                rgba(255,255,255,0.08);

            transform:
                rotate(3deg);

            animation:
                floatCard 5s ease-in-out infinite;
        }


        @keyframes floatCard {

            0%, 100% {

                transform:
                    rotate(3deg)
                    translateY(0);
            }

            50% {

                transform:
                    rotate(1deg)
                    translateY(-15px);
            }
        }


        .food-scene {

            height:
                60%;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            font-size:
                130px;

            background:

                radial-gradient(
                    circle,
                    rgba(245,166,35,0.30),
                    transparent 60%
                );
        }


        .dashboard-preview {

            position:
                absolute;

            bottom:
                0;

            left:
                0;

            width:
                100%;

            padding:
                25px;

            background:
                rgba(10,10,12,0.92);

            border-top:
                1px solid
                rgba(255,255,255,0.08);
        }


        .preview-title {

            font-size:
                12px;

            color:
                #888;

            margin-bottom:
                8px;
        }


        .preview-total {

            font-size:
                30px;

            font-weight:
                800;
        }


        .preview-total span {

            color:
                #f5a623;
        }


        .preview-line {

            height:
                1px;

            background:
                rgba(255,255,255,0.08);

            margin:
                15px 0;
        }


        .preview-row {

            display:
                flex;

            justify-content:
                space-between;

            color:
                #aaa;

            font-size:
                13px;
        }


        /* ================= SLIDER ================= */

        .slider {

            margin-top:
                45px;

            display:
                flex;

            align-items:
                center;

            gap:
                10px;
        }


        .dot {

            width:
                8px;

            height:
                8px;

            border-radius:
                50%;

            background:
                #555;
        }


        .dot.active {

            width:
                28px;

            border-radius:
                20px;

            background:
                #f5a623;
        }


        /* ================= SECTION ================= */

        .section {

            padding:
                110px 7%;
        }


        .section-header {

            text-align:
                center;

            max-width:
                700px;

            margin:
                auto auto 65px;
        }


        .section-label {

            color:
                #f5a623;

            font-size:
                13px;

            font-weight:
                800;

            letter-spacing:
                2px;

            text-transform:
                uppercase;

            margin-bottom:
                15px;
        }


        .section h2 {

            font-size:
                clamp(35px, 4vw, 55px);

            margin-bottom:
                18px;
        }


        .section-header p {

            color:
                #85858c;

            line-height:
                1.7;
        }


        /* ================= FEATURES ================= */

        .features {

            display:
                grid;

            grid-template-columns:
                repeat(4, 1fr);

            gap:
                20px;
        }


        .feature {

            padding:
                32px;

            min-height:
                230px;

            border-radius:
                20px;

            background:
                #111114;

            border:
                1px solid
                rgba(255,255,255,0.07);

            transition:
                0.35s;
        }


        .feature:hover {

            transform:
                translateY(-8px);

            border-color:
                rgba(245,166,35,0.35);

            box-shadow:
                0 20px 50px
                rgba(0,0,0,0.3);
        }


        .feature-icon {

            width:
                55px;

            height:
                55px;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            border-radius:
                15px;

            background:
                rgba(245,166,35,0.12);

            font-size:
                25px;

            margin-bottom:
                25px;
        }


        .feature h3 {

            margin-bottom:
                12px;
        }


        .feature p {

            color:
                #85858c;

            line-height:
                1.6;

            font-size:
                14px;
        }


        /* ================= QUOTE ================= */

        .quote-section {

            padding:
                100px 7%;

            text-align:
                center;

            background:

                linear-gradient(
                    135deg,
                    #15120d,
                    #0b0b0d
                );
        }


        .quote {

            max-width:
                900px;

            margin:
                auto;

            font-size:
                clamp(28px, 4vw, 50px);

            line-height:
                1.25;

            font-weight:
                700;
        }


        .quote span {

            color:
                #f5a623;
        }


        /* ================= ABOUT ================= */

        .about {

            display:
                grid;

            grid-template-columns:
                1fr 1fr;

            gap:
                70px;

            align-items:
                center;
        }


        .about-box {

            padding:
                40px;

            border-radius:
                25px;

            background:
                #111114;

            border:
                1px solid
                rgba(255,255,255,0.08);
        }


        .about-box h3 {

            font-size:
                27px;

            margin-bottom:
                20px;
        }


        .about-box p {

            color:
                #909097;

            line-height:
                1.8;
        }


        .creator {

            color:
                #f5a623;

            font-weight:
                800;
        }


        /* ================= CTA ================= */

        .cta {

            margin:
                0 7% 100px;

            padding:
                75px 50px;

            text-align:
                center;

            border-radius:
                30px;

            background:

                radial-gradient(
                    circle at center,
                    rgba(245,166,35,0.16),
                    transparent 60%
                ),

                #111114;

            border:
                1px solid
                rgba(245,166,35,0.18);
        }


        .cta h2 {

            font-size:
                clamp(32px, 4vw, 52px);

            margin-bottom:
                18px;
        }


        .cta p {

            color:
                #888;

            margin-bottom:
                30px;
        }


        /* ================= FOOTER ================= */

        footer {

            padding:
                35px 7%;

            border-top:
                1px solid
                rgba(255,255,255,0.07);

            display:
                flex;

            justify-content:
                space-between;

            align-items:
                center;

            color:
                #666;

            font-size:
                13px;
        }


        footer strong {

            color:
                #aaa;
        }


        /* ================= RESPONSIVE ================= */

        @media(max-width: 1000px) {

            .hero-content {

                width:
                    100%;
            }


            .hero-visual {

                opacity:
                    0.22;

                width:
                    70%;
            }


            .features {

                grid-template-columns:
                    repeat(2, 1fr);
            }


            .about {

                grid-template-columns:
                    1fr;
            }


            .nav-links a:not(.nav-login) {

                display:
                    none;
            }
        }


        @media(max-width: 600px) {

            nav {

                padding:
                    0 5%;
            }


            .hero {

                padding-left:
                    5%;

                padding-right:
                    5%;
            }


            .hero h1 {

                letter-spacing:
                    -2px;
            }


            .hero p {

                font-size:
                    16px;
            }


            .hero-visual {

                right:
                    -15%;

                width:
                    100%;
            }


            .features {

                grid-template-columns:
                    1fr;
            }


            .section {

                padding:
                    80px 5%;
            }


            .cta {

                margin-left:
                    5%;

                margin-right:
                    5%;

                padding:
                    55px 25px;
            }


            footer {

                flex-direction:
                    column;

                gap:
                    10px;

                text-align:
                    center;
            }

        }

    </style>

</head>


<body>


<!-- ================= NAVBAR ================= -->

<nav>

    <div class="logo">

        Resto<span>Bill</span>

    </div>


    <div class="nav-links">

        <a href="#features">
            Features
        </a>

        <a href="#about">
            About
        </a>

        <a
            href="/login"
            class="nav-login">

            Login

        </a>

    </div>

</nav>


<!-- ================= HERO ================= -->

<section class="hero">


    <div class="hero-content">


        <div class="badge">

            RESTAURANT MANAGEMENT SYSTEM

        </div>


        <h1>

            Manage your restaurant.

            <br>

            <span>
                Smarter.
            </span>

        </h1>


        <p>

            A modern restaurant billing and management
            system designed to make billing faster,
            inventory easier and daily operations smoother.

        </p>


        <div class="hero-buttons">


            <a
                href="/login"
                class="primary-btn">

                Get Started →

            </a>


            <a
                href="#features"
                class="secondary-btn">

                Explore System

            </a>


        </div>


        <div class="slider">

            <div class="dot active"></div>

            <div class="dot"></div>

            <div class="dot"></div>

        </div>


    </div>


    <div class="hero-visual">


        <div class="restaurant-card">


            <div class="food-scene">

                🍕

            </div>


            <div class="dashboard-preview">


                <div class="preview-title">

                    TODAY'S SALES

                </div>


                <div class="preview-total">

                    ₹<span>24,850</span>

                </div>


                <div class="preview-line"></div>


                <div class="preview-row">

                    <span>
                        Bills Generated
                    </span>

                    <span>
                        128
                    </span>

                </div>


                <br>


                <div class="preview-row">

                    <span>
                        Orders
                    </span>

                    <span>
                        156
                    </span>

                </div>


            </div>


        </div>


    </div>


</section>


<!-- ================= FEATURES ================= -->

<section
    class="section"
    id="features">


    <div class="section-header">


        <div class="section-label">

            Everything You Need

        </div>


        <h2>

            One system.

            <br>

            Complete control.

        </h2>


        <p>

            From taking an order to generating an invoice,
            manage your restaurant operations from one
            simple dashboard.

        </p>


    </div>


    <div class="features">


        <div class="feature">


            <div class="feature-icon">

                🧾

            </div>


            <h3>

                Smart Billing

            </h3>


            <p>

                Generate accurate bills and invoices
                quickly with an easy-to-use billing
                interface.

            </p>


        </div>


        <div class="feature">


            <div class="feature-icon">

                👥

            </div>


            <h3>

                Customers

            </h3>


            <p>

                Keep customer information organized
                and make restaurant management easier.

            </p>


        </div>


        <div class="feature">


            <div class="feature-icon">

                📦

            </div>


            <h3>

                Inventory

            </h3>


            <p>

                Keep track of menu items, pricing and
                inventory from one centralized system.

            </p>


        </div>


        <div class="feature">


            <div class="feature-icon">

                📊

            </div>


            <h3>

                Reports

            </h3>


            <p>

                Turn restaurant activity into useful
                insights and understand your business
                better.

            </p>


        </div>


    </div>


</section>


<!-- ================= QUOTE ================= -->

<section class="quote-section">


    <div class="quote">

        "Good restaurants create great food.

        <br>

        <span>
            Great systems create great restaurants.
        </span>"

    </div>


</section>


<!-- ================= ABOUT ================= -->

<section
    class="section"
    id="about">


    <div class="about">


        <div>


            <div class="section-label">

                About The Project

            </div>


            <h2>

                Built with a simple idea.

            </h2>


            <p style="
                color:#888;
                line-height:1.8;
                margin-top:20px;
            ">

                Make restaurant management simpler,
                faster and more organized.

                This system combines billing,
                menu management, customers,
                inventory and reporting into one
                modern platform.

            </p>


        </div>


        <div class="about-box">


            <h3>

                Crafted with passion.

            </h3>


            <p>

                Restaurant Billing System is a
                software project developed by

                <span class="creator">

                    Abhijeet Gutte

                </span>.

                <br><br>

                The goal is to build a practical,
                reliable and modern solution for
                real-world restaurant operations.

            </p>


        </div>


    </div>


</section>


<!-- ================= CTA ================= -->

<section class="cta">


    <h2>

        Ready to manage smarter?

    </h2>


    <p>

        Step into your restaurant management dashboard.

    </p>


    <a
        href="/login"
        class="primary-btn">

        Login to Dashboard →

    </a>


</section>


<!-- ================= FOOTER ================= -->

<footer>


    <div>

        © 2026

        <strong>
            RestoBill
        </strong>

    </div>


    <div>

        Designed & Developed by

        <strong>
            Abhijeet Gutte
        </strong>

    </div>


</footer>


<!-- ================= SLIDESHOW SCRIPT ================= -->

<script>

    const dots =
        document.querySelectorAll(".dot");

    let currentSlide = 0;


    setInterval(function() {

        dots.forEach(function(dot) {

            dot.classList.remove("active");

        });


        currentSlide++;


        if (currentSlide >= dots.length) {

            currentSlide = 0;

        }


        dots[currentSlide]
            .classList.add("active");


    }, 2500);

</script>


</body>

</html>
"""


@app.route("/dashboard")
@login_required
def dashboard():

    total_menu = Menu.query.count()

    total_customers = Customer.query.count()

    today = datetime.now().date()

    # ==========================================
    # TODAY'S BILLS
    # ==========================================

    today_bills = Bill.query.filter(
        db.func.date(Bill.created_at) == today
    ).all()

    today_orders = len(today_bills)

    today_sales = sum(
        bill.grand_total or 0
        for bill in today_bills
    )

    # ==========================================
    # TODAY'S INVENTORY
    # ==========================================

    inventory_items = Inventory.query.filter_by(
        stock_date=today
    ).all()

    total_inventory = len(inventory_items)

    # ==========================================
    # LOW STOCK
    # ==========================================

    low_stock_items = [
        item
        for item in inventory_items
        if item.current_quantity > 0
        and item.current_quantity <= item.minimum_stock
    ]

    # ==========================================
    # OUT OF STOCK
    # ==========================================

    out_of_stock_items = [
        item
        for item in inventory_items
        if item.current_quantity <= 0
    ]

    low_stock_count = len(low_stock_items)

    out_of_stock_count = len(out_of_stock_items)

    # ==========================================
    # DASHBOARD
    # ==========================================

    return render_template(
        "dashboard.html",

        total_menu=total_menu,

        total_customers=total_customers,

        total_orders=Bill.query.count(),

        today_orders=today_orders,

        today_sales=today_sales,

        total_inventory=total_inventory,

        low_stock_count=low_stock_count,

        out_of_stock_count=out_of_stock_count,

        low_stock_items=low_stock_items,

        out_of_stock_items=out_of_stock_items
    )
    


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)