from flask import Blueprint, render_template
from flask_login import login_required

from models.models import Menu

billing = Blueprint("billing", __name__)


@billing.route("/billing")
@login_required
def billing_page():
    items = Menu.query.all()

    return render_template(
        "billing.html",
        items=items
    )