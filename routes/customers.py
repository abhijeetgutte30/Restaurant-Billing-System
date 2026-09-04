from flask import Blueprint, render_template
from flask_login import login_required

from models.models import Customer, Bill


# =========================================================
# CUSTOMERS BLUEPRINT
# =========================================================

customers = Blueprint(
    "customers",
    __name__
)


# =========================================================
# CUSTOMERS PAGE
# =========================================================

@customers.route("/customers")
@login_required
def customers_page():

    # Latest customers first
    customer_list = (
        Customer.query
        .order_by(Customer.id.desc())
        .all()
    )

    return render_template(
        "customers.html",
        customers=customer_list
    )


# =========================================================
# CUSTOMER BILL HISTORY
# =========================================================

@customers.route("/customers/<int:customer_id>/history")
@login_required
def customer_history(customer_id):

    # Find customer
    customer = Customer.query.get_or_404(
        customer_id
    )

    # Get all bills of this customer
    bills = (
        Bill.query
        .join(
            Customer,
            Customer.bill_id == Bill.id
        )
        .filter(
            Customer.id == customer_id
        )
        .order_by(
            Bill.id.desc()
        )
        .all()
    )

    return render_template(
        "customer_history.html",
        customer=customer,
        bills=bills
    )