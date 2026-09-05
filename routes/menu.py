from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from database.database import db
from models.models import Menu


menu = Blueprint("menu", __name__)


# =========================================================
# MENU LIST
# =========================================================

@menu.route("/menu")
@login_required
def menu_list():

    items = Menu.query.order_by(
        Menu.id.desc()
    ).all()

    return render_template(
        "menu.html",
        items=items
    )


# =========================================================
# ADD MENU ITEM
# =========================================================

@menu.route(
    "/add-menu",
    methods=["POST"]
)
@login_required
def add_menu():

    name = request.form.get(
        "name",
        ""
    ).strip()

    category = request.form.get(
        "category",
        ""
    ).strip()

    price = request.form.get(
        "price",
        ""
    ).strip()


    # VALIDATION
    if not name or not category or not price:

        flash(
            "Please fill all fields.",
            "error"
        )

        return redirect(
            url_for("menu.menu_list")
        )


    try:

        price = float(price)

    except ValueError:

        flash(
            "Price must be a valid number.",
            "error"
        )

        return redirect(
            url_for("menu.menu_list")
        )


    if price < 0:

        flash(
            "Price cannot be negative.",
            "error"
        )

        return redirect(
            url_for("menu.menu_list")
        )


    # CREATE MENU ITEM
    item = Menu(
        name=name,
        category=category,
        price=price
    )


    db.session.add(item)
    db.session.commit()


    flash(
        f"{name} added successfully.",
        "success"
    )


    return redirect(
        url_for("menu.menu_list")
    )


# =========================================================
# UPDATE MENU ITEM
# =========================================================

@menu.route(
    "/update-menu/<int:item_id>",
    methods=["POST"]
)
@login_required
def update_menu(item_id):

    item = Menu.query.get_or_404(
        item_id
    )


    name = request.form.get(
        "name",
        ""
    ).strip()

    category = request.form.get(
        "category",
        ""
    ).strip()

    price = request.form.get(
        "price",
        ""
    ).strip()


    if not name or not category or not price:

        flash(
            "Please fill all fields.",
            "error"
        )

        return redirect(
            url_for("menu.menu_list")
        )


    try:

        price = float(price)

    except ValueError:

        flash(
            "Price must be a valid number.",
            "error"
        )

        return redirect(
            url_for("menu.menu_list")
        )


    if price < 0:

        flash(
            "Price cannot be negative.",
            "error"
        )

        return redirect(
            url_for("menu.menu_list")
        )


    item.name = name
    item.category = category
    item.price = price


    db.session.commit()


    flash(
        f"{name} updated successfully.",
        "success"
    )


    return redirect(
        url_for("menu.menu_list")
    )


# =========================================================
# DELETE MENU ITEM
# =========================================================

@menu.route(
    "/delete-menu/<int:item_id>",
    methods=["POST"]
)
@login_required
def delete_menu(item_id):

    item = Menu.query.get_or_404(
        item_id
    )


    item_name = item.name


    db.session.delete(item)
    db.session.commit()


    flash(
        f"{item_name} deleted successfully.",
        "success"
    )


    return redirect(
        url_for("menu.menu_list")
    )