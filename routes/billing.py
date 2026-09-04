from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required

from database.database import db
from models.models import Menu, Bill, BillItem


billing = Blueprint("billing", __name__)


# ==========================================
# BILLING PAGE
# ==========================================

@billing.route("/billing")
@login_required
def billing_page():

    items = Menu.query.all()

    return render_template(
        "billing.html",
        items=items
    )


# ==========================================
# SAVE / GENERATE BILL
# ==========================================

@billing.route("/billing/generate", methods=["POST"])
@login_required
def generate_bill():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "No bill data received."
            }), 400


        items = data.get("items", [])

        if not items:
            return jsonify({
                "success": False,
                "message": "Cart is empty."
            }), 400


        # --------------------------------------
        # BILL VALUES
        # --------------------------------------

        subtotal = float(data.get("subtotal", 0))
        gst = float(data.get("gst", 0))
        discount = float(data.get("discount", 0))
        grand_total = float(data.get("grand_total", 0))

        payment_method = data.get(
            "payment_method",
            "Cash"
        )


        # --------------------------------------
        # VALIDATE PAYMENT METHOD
        # --------------------------------------

        allowed_payment_methods = [
            "Cash",
            "UPI",
            "Card"
        ]

        if payment_method not in allowed_payment_methods:

            payment_method = "Cash"


        # --------------------------------------
        # GENERATE INVOICE NUMBER
        # --------------------------------------

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


        # --------------------------------------
        # CREATE BILL
        # --------------------------------------

        new_bill = Bill(

            invoice_number=invoice_number,

            subtotal=subtotal,

            gst=gst,

            discount=discount,

            grand_total=grand_total,

            payment_method=payment_method

        )


        db.session.add(new_bill)

        db.session.flush()


        # --------------------------------------
        # SAVE BILL ITEMS
        # --------------------------------------

        for item in items:

            menu_item_id = item.get("id")

            quantity = int(
                item.get("quantity", 1)
            )


            menu_item = Menu.query.get(
                menu_item_id
            )


            if not menu_item:

                continue


            price = float(
                menu_item.price
            )


            item_total = (
                price * quantity
            )


            bill_item = BillItem(

                bill_id=new_bill.id,

                menu_item_id=menu_item.id,

                item_name=menu_item.name,

                price=price,

                quantity=quantity,

                total=item_total

            )


            db.session.add(bill_item)


        # --------------------------------------
        # SAVE EVERYTHING
        # --------------------------------------

        db.session.commit()


        print("INVOICE DEBUG:", invoice_number, grand_total, payment_method)


        return jsonify({

            "success": True,

            "message": "Bill generated successfully.",

            "invoice_number": invoice_number,

            "total": grand_total,

            "payment_method": payment_method

        })


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