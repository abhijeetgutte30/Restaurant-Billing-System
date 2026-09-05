from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from datetime import date

from database.database import db
from models.models import Inventory


inventory = Blueprint("inventory", __name__)


# =========================================================
# INVENTORY PAGE
# =========================================================

@inventory.route("/inventory")
@login_required
def inventory_list():

    today = date.today()

    # -----------------------------------------------------
    # TODAY'S STOCK
    # -----------------------------------------------------

    items = Inventory.query.filter_by(
        stock_date=today
    ).order_by(
        Inventory.id.desc()
    ).all()


    # -----------------------------------------------------
    # AUTOMATICALLY CREATE TODAY'S RECORD
    # FROM PREVIOUS CLOSING STOCK
    # -----------------------------------------------------

    all_previous_items = Inventory.query.filter(
        Inventory.stock_date < today
    ).all()

    existing_names = {
        item.name.lower()
        for item in items
    }

    for previous in all_previous_items:

        if previous.name.lower() in existing_names:
            continue

        new_item = Inventory(

            name=previous.name,

            category=previous.category,

            opening_quantity=previous.current_quantity,

            added_quantity=0,

            current_quantity=previous.current_quantity,

            unit=previous.unit,

            minimum_stock=previous.minimum_stock,

            stock_date=today
        )

        db.session.add(new_item)

        items.append(new_item)

        existing_names.add(
            previous.name.lower()
        )


    db.session.commit()


    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    total_items = len(items)

    low_stock_items = [
        item
        for item in items
        if item.current_quantity > 0
        and item.current_quantity <= item.minimum_stock
    ]

    out_of_stock_items = [
        item
        for item in items
        if item.current_quantity <= 0
    ]


    # -----------------------------------------------------
    # RENDER PAGE
    # -----------------------------------------------------

    return render_template(

        "inventory.html",

        items=items,

        total_items=total_items,

        low_stock_items=low_stock_items,

        low_stock_count=len(low_stock_items),

        out_of_stock_items=out_of_stock_items,

        out_of_stock_count=len(out_of_stock_items),

        today=today
    )


# =========================================================
# ADD NEW INVENTORY ITEM
# =========================================================

@inventory.route(
    "/add-inventory",
    methods=["POST"]
)
@login_required
def add_inventory():

    name = request.form.get(
        "name",
        ""
    ).strip()

    category = request.form.get(
        "category",
        ""
    ).strip()

    quantity = request.form.get(
        "quantity",
        ""
    ).strip()

    unit = request.form.get(
        "unit",
        ""
    ).strip()

    minimum_stock = request.form.get(
        "minimum_stock",
        "0"
    ).strip()


    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not name or not category or not quantity or not unit:

        flash(
            "Please fill all required fields.",
            "error"
        )

        return redirect(
            url_for("inventory.inventory_list")
        )


    try:

        quantity = float(quantity)

        minimum_stock = float(
            minimum_stock or 0
        )

    except ValueError:

        flash(
            "Quantity and minimum stock must be valid numbers.",
            "error"
        )

        return redirect(
            url_for("inventory.inventory_list")
        )


    if quantity < 0 or minimum_stock < 0:

        flash(
            "Quantity cannot be negative.",
            "error"
        )

        return redirect(
            url_for("inventory.inventory_list")
        )


    today = date.today()


    # -----------------------------------------------------
    # CHECK IF ITEM ALREADY EXISTS TODAY
    # -----------------------------------------------------

    existing_item = Inventory.query.filter(
        db.func.lower(Inventory.name)
        == name.lower(),
        Inventory.stock_date == today
    ).first()


    if existing_item:

        flash(
            f"{name} already exists in today's inventory.",
            "error"
        )

        return redirect(
            url_for("inventory.inventory_list")
        )


    # -----------------------------------------------------
    # FIND PREVIOUS DAY'S STOCK
    # -----------------------------------------------------

    previous_item = Inventory.query.filter(
        db.func.lower(Inventory.name)
        == name.lower(),
        Inventory.stock_date < today
    ).order_by(
        Inventory.stock_date.desc()
    ).first()


    if previous_item:

        opening_quantity = previous_item.current_quantity

    else:

        opening_quantity = 0


    # -----------------------------------------------------
    # CREATE TODAY'S STOCK
    # -----------------------------------------------------

    item = Inventory(

        name=name,

        category=category,

        opening_quantity=opening_quantity,

        added_quantity=quantity,

        current_quantity=(
            opening_quantity + quantity
        ),

        unit=unit,

        minimum_stock=minimum_stock,

        stock_date=today
    )


    db.session.add(item)

    db.session.commit()


    flash(
        f"{name} added successfully.",
        "success"
    )


    return redirect(
        url_for("inventory.inventory_list")
    )


# =========================================================
# ADD MORE STOCK TODAY
# =========================================================

@inventory.route(
    "/add-stock/<int:item_id>",
    methods=["POST"]
)
@login_required
def add_stock(item_id):

    item = Inventory.query.get_or_404(
        item_id
    )


    quantity = request.form.get(
        "quantity",
        ""
    ).strip()


    if not quantity:

        flash(
            "Please enter quantity.",
            "error"
        )

        return redirect(
            url_for("inventory.inventory_list")
        )


    try:

        quantity = float(quantity)

    except ValueError:

        flash(
            "Quantity must be a valid number.",
            "error"
        )

        return redirect(
            url_for("inventory.inventory_list")
        )


    if quantity <= 0:

        flash(
            "Quantity must be greater than zero.",
            "error"
        )

        return redirect(
            url_for("inventory.inventory_list")
        )


    # -----------------------------------------------------
    # ADD STOCK
    # -----------------------------------------------------

    item.added_quantity += quantity

    item.current_quantity += quantity


    db.session.commit()


    flash(
        f"{item.name}: {quantity:g} {item.unit} stock added.",
        "success"
    )


    return redirect(
        url_for("inventory.inventory_list")
    )


# =========================================================
# UPDATE CURRENT STOCK
# =========================================================

@inventory.route(
    "/update-inventory/<int:item_id>",
    methods=["POST"]
)
@login_required
def update_inventory(item_id):

    item = Inventory.query.get_or_404(
        item_id
    )


    quantity = request.form.get(
        "quantity",
        ""
    ).strip()


    if not quantity:

        flash(
            "Please enter quantity.",
            "error"
        )

        return redirect(
            url_for("inventory.inventory_list")
        )


    try:

        quantity = float(quantity)

    except ValueError:

        flash(
            "Quantity must be a valid number.",
            "error"
        )

        return redirect(
            url_for("inventory.inventory_list")
        )


    if quantity < 0:

        flash(
            "Quantity cannot be negative.",
            "error"
        )

        return redirect(
            url_for("inventory.inventory_list")
        )


    # -----------------------------------------------------
    # MANUALLY SET CURRENT CLOSING STOCK
    # -----------------------------------------------------

    item.current_quantity = quantity


    db.session.commit()


    if quantity == 0:

        flash(
            f"{item.name} is Out of Stock.",
            "error"
        )

    elif quantity <= item.minimum_stock:

        flash(
            f"{item.name} is now Low Stock.",
            "success"
        )

    else:

        flash(
            f"{item.name} stock updated successfully.",
            "success"
        )


    return redirect(
        url_for("inventory.inventory_list")
    )


# =========================================================
# DELETE TODAY'S INVENTORY ITEM
# =========================================================

@inventory.route(
    "/delete-inventory/<int:item_id>",
    methods=["POST"]
)
@login_required
def delete_inventory(item_id):

    item = Inventory.query.get_or_404(
        item_id
    )


    item_name = item.name


    db.session.delete(item)

    db.session.commit()


    flash(
        f"{item_name} deleted from today's inventory.",
        "success"
    )


    return redirect(
        url_for("inventory.inventory_list")
    )