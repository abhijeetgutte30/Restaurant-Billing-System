from database.database import db
from flask_login import UserMixin
from config import bcrypt, login_manager


# ==========================================
# ADMIN MODEL
# ==========================================

class Admin(UserMixin, db.Model):

    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(
            self.password,
            password
        )


# ==========================================
# MENU MODEL
# ==========================================

class Menu(db.Model):

    __tablename__ = "menu"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )


# ==========================================
# BILL MODEL
# ==========================================

class Bill(db.Model):

    __tablename__ = "bills"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    invoice_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    subtotal = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    gst = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    discount = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    grand_total = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    payment_method = db.Column(
        db.String(20),
        nullable=False,
        default="Cash"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # Relationship with BillItem
    items = db.relationship(
        "BillItem",
        backref="bill",
        lazy=True,
        cascade="all, delete-orphan"
    )


# ==========================================
# BILL ITEM MODEL
# ==========================================

class BillItem(db.Model):

    __tablename__ = "bill_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    bill_id = db.Column(
        db.Integer,
        db.ForeignKey("bills.id"),
        nullable=False
    )

    menu_item_id = db.Column(
        db.Integer,
        db.ForeignKey("menu.id"),
        nullable=False
    )

    item_name = db.Column(
        db.String(100),
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    total = db.Column(
        db.Float,
        nullable=False
    )


# ==========================================
# LOGIN USER LOADER
# ==========================================

@login_manager.user_loader
def load_user(user_id):

    return Admin.query.get(int(user_id))