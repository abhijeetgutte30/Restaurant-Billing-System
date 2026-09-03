from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from database.database import db
from models.models import Menu

menu = Blueprint("menu", __name__)


@menu.route("/menu")
@login_required
def menu_list():

    items = Menu.query.all()

    return render_template("menu.html", items=items)


@menu.route("/add-menu", methods=["GET", "POST"])
@login_required
def add_menu():

    if request.method == "POST":

        name = request.form.get("name")
        category = request.form.get("category")
        price = request.form.get("price")

        item = Menu(
            name=name,
            category=category,
            price=price
        )

        db.session.add(item)
        db.session.commit()

        return redirect(url_for("menu.menu_list"))

    return render_template("add_menu.html")
@menu.route("/delete-menu/<int:id>")
@login_required
def delete_menu(id):

    item = Menu.query.get_or_404(id)

    db.session.delete(item)

    db.session.commit()

    return redirect(url_for("menu.menu_list"))