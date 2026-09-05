from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required

from database.database import db
from models.models import Menu, Bill, BillItem, Customer, Inventory


billing = Blueprint("billing", __name__)


# =========================================================
# BILLING PAGE
# =========================================================

@billing.route("/billing")
@login_required
def billing_page():

    items = Menu.query.all()

    return render_template(
        "billing.html",
        items=items
    )


# =========================================================
# GENERATE BILL
# =========================================================

@billing.route("/billing/generate", methods=["POST"])
@login_required
def generate_bill():

    try:

        # -------------------------------------------------
        # GET DATA FROM FRONTEND
        # -------------------------------------------------

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "No bill data received."
            }), 400


        # -------------------------------------------------
        # CART ITEMS
        # -------------------------------------------------

        items = data.get("items", [])

        if not items:
            return jsonify({
                "success": False,
                "message": "Cart is empty."
            }), 400


        # -------------------------------------------------
        # CUSTOMER DETAILS
        # -------------------------------------------------

        customer_name = str(
            data.get("customer_name", "")
        ).strip()

        mobile = str(
            data.get("mobile", "")
        ).strip()

        table_no = str(
            data.get("table_no", "")
        ).strip()


        # -------------------------------------------------
        # VALIDATE CUSTOMER DETAILS
        # -------------------------------------------------

        if not customer_name:
            return jsonify({
                "success": False,
                "message": "Please enter customer name."
            }), 400


        if not mobile:
            return jsonify({
                "success": False,
                "message": "Please enter mobile number."
            }), 400


        if not table_no:
            return jsonify({
                "success": False,
                "message": "Please enter table number."
            }), 400


        # -------------------------------------------------
        # BILL AMOUNTS
        # -------------------------------------------------

        subtotal = float(
            data.get("subtotal", 0)
        )

        gst = float(
            data.get("gst", 0)
        )

        discount = float(
            data.get("discount", 0)
        )

        grand_total = float(
            data.get("grand_total", 0)
        )


        # -------------------------------------------------
        # PAYMENT METHOD
        # -------------------------------------------------

        payment_method = data.get(
            "payment_method",
            "Cash"
        )

        allowed_payment_methods = [
            "Cash",
            "UPI",
            "Card"
        ]

        if payment_method not in allowed_payment_methods:
            payment_method = "Cash"


        # -------------------------------------------------
        # GENERATE INVOICE NUMBER
        # -------------------------------------------------

        last_bill = (
            Bill.query
            .order_by(Bill.id.desc())
            .first()
        )

        if last_bill:
            next_number = last_bill.id + 1
        else:
            next_number = 1

        invoice_number = (
            f"INV-{next_number:05d}"
        )


        # =================================================
        # CHECK INVENTORY BEFORE CREATING BILL
        # =================================================

        stock_updates = []

        for item in items:

            menu_item_id = item.get("id")

            try:
                quantity = int(
                    item.get("quantity", 1)
                )
            except (ValueError, TypeError):

                return jsonify({
                    "success": False,
                    "message": "Invalid item quantity."
                }), 400


            if quantity <= 0:

                return jsonify({
                    "success": False,
                    "message": "Item quantity must be greater than zero."
                }), 400


            # ---------------------------------------------
            # FIND MENU ITEM
            # ---------------------------------------------

            menu_item = Menu.query.get(
                menu_item_id
            )

            if not menu_item:

                return jsonify({
                    "success": False,
                    "message": "One of the selected menu items was not found."
                }), 400


            # ---------------------------------------------
            # FIND INVENTORY ITEM BY NAME
            # ---------------------------------------------

            inventory_item = Inventory.query.filter(
                db.func.lower(Inventory.name)
                == menu_item.name.lower()
            ).first()


            # ---------------------------------------------
            # INVENTORY ITEM NOT FOUND
            # ---------------------------------------------

            if not inventory_item:

                return jsonify({
                    "success": False,
                    "message": (
                        f"{menu_item.name} is not available "
                        f"in Inventory. Please add it first."
                    )
                }), 400


            # ---------------------------------------------
            # CHECK AVAILABLE STOCK
            # ---------------------------------------------

            if inventory_item.quantity < quantity:

                return jsonify({
                    "success": False,
                    "message": (
                        f"Not enough stock for {menu_item.name}. "
                        f"Available: {inventory_item.quantity:g} "
                        f"{inventory_item.unit}"
                    )
                }), 400


            # Save update for later
            stock_updates.append({
                "inventory_item": inventory_item,
                "quantity": quantity,
                "menu_item": menu_item
            })


        # =================================================
        # CREATE BILL
        # =================================================

        new_bill = Bill(

            invoice_number=invoice_number,

            subtotal=subtotal,

            gst=gst,

            discount=discount,

            grand_total=grand_total,

            payment_method=payment_method
        )

        db.session.add(new_bill)

        # Get new bill ID
        db.session.flush()


        # =================================================
        # CREATE BILL ITEMS + UPDATE INVENTORY
        # =================================================

        for stock in stock_updates:

            inventory_item = stock["inventory_item"]
            quantity = stock["quantity"]
            menu_item = stock["menu_item"]


            # ---------------------------------------------
            # CALCULATE ITEM TOTAL
            # ---------------------------------------------

            price = float(
                menu_item.price
            )

            item_total = (
                price * quantity
            )


            # ---------------------------------------------
            # CREATE BILL ITEM
            # ---------------------------------------------

            bill_item = BillItem(

                bill_id=new_bill.id,

                menu_item_id=menu_item.id,

                item_name=menu_item.name,

                price=price,

                quantity=quantity,

                total=item_total
            )

            db.session.add(
                bill_item
            )


            # ---------------------------------------------
            # DEDUCT INVENTORY
            # ---------------------------------------------

            inventory_item.quantity -= quantity


        # =================================================
        # CREATE CUSTOMER
        # =================================================

        new_customer = Customer(

            name=customer_name,

            mobile=mobile,

            table_no=table_no,

            bill_id=new_bill.id
        )

        db.session.add(
            new_customer
        )


        # =================================================
        # SAVE EVERYTHING
        # =================================================

        db.session.commit()


        # =================================================
        # SUCCESS RESPONSE
        # =================================================

        return jsonify({

            "success": True,

            "message": (
                "Bill generated successfully "
                "and inventory updated."
            ),

            "invoice_number": invoice_number,

            "total": grand_total,

            "payment_method": payment_method,

            "customer_name": customer_name,

            "mobile": mobile,

            "table_no": table_no

        })


    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as e:

        db.session.rollback()

        print(
            "BILL GENERATION ERROR:",
            e
        )

        return jsonify({

            "success": False,

            "message": "Unable to generate bill."

        }), 500