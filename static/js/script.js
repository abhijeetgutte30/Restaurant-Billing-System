// ==========================================
// RESTAURANT BILLING SYSTEM
// BILLING JAVASCRIPT
// ==========================================

let cart = [];
let selectedPayment = "Cash";


// ==========================================
// ADD ITEM TO CART
// ==========================================

function addToCart(id, name, price) {

    const existingItem = cart.find(item => item.id === id);

    if (existingItem) {

        existingItem.quantity++;

    } else {

        cart.push({
            id: id,
            name: name,
            price: Number(price),
            quantity: 1
        });

    }

    updateCart();

}



// ==========================================
// UPDATE CART
// ==========================================

function updateCart() {

    const cartContainer = document.getElementById("cartItems");

    if (!cartContainer) {
        return;
    }


    cartContainer.innerHTML = "";


    if (cart.length === 0) {

        cartContainer.innerHTML = `

            <div class="empty-cart">

                <div class="empty-cart-icon">
                    🛒
                </div>

                <h3>
                    Cart is Empty
                </h3>

                <p>
                    Select items from the menu
                    to start billing.
                </p>

            </div>

        `;

    }


    let itemCount = 0;


    cart.forEach(item => {

        itemCount += item.quantity;


        const cartItem = document.createElement("div");

        cartItem.className = "cart-item";


        cartItem.innerHTML = `

            <div class="cart-item-info">

                <strong>
                    ${item.name}
                </strong>

                <span>
                    ₹${item.price.toFixed(2)}
                </span>

            </div>


            <div class="quantity-control">

                <button
                    type="button"
                    onclick="changeQuantity(${item.id}, -1)">
                    −
                </button>

                <span>
                    ${item.quantity}
                </span>

                <button
                    type="button"
                    onclick="changeQuantity(${item.id}, 1)">
                    +
                </button>

            </div>


            <strong class="cart-item-total">

                ₹${(item.price * item.quantity).toFixed(2)}

            </strong>

        `;


        cartContainer.appendChild(cartItem);

    });


    const cartCount = document.getElementById("cartCount");


    if (cartCount) {

        cartCount.innerText =
            `${itemCount} ${itemCount === 1 ? "Item" : "Items"}`;

    }


    calculateBill();

}



// ==========================================
// CHANGE QUANTITY
// ==========================================

function changeQuantity(id, change) {

    const item = cart.find(item => item.id === id);


    if (!item) {
        return;
    }


    item.quantity += change;


    if (item.quantity <= 0) {

        cart = cart.filter(item => item.id !== id);

    }


    updateCart();

}



// ==========================================
// CALCULATE BILL
// ==========================================

function calculateBill() {

    let subtotal = 0;


    cart.forEach(item => {

        subtotal += item.price * item.quantity;

    });


    const gst = subtotal * 0.05;


    const discountInput =
        document.getElementById("discount");


    let discount = 0;


    if (discountInput) {

        discount = Number(discountInput.value) || 0;

    }


    let grandTotal =
        subtotal + gst - discount;


    if (grandTotal < 0) {

        grandTotal = 0;

    }


    const subtotalElement =
        document.getElementById("subtotal");

    const gstElement =
        document.getElementById("gst");

    const totalElement =
        document.getElementById("grandTotal");


    if (subtotalElement) {

        subtotalElement.innerText =
            `₹${subtotal.toFixed(2)}`;

    }


    if (gstElement) {

        gstElement.innerText =
            `₹${gst.toFixed(2)}`;

    }


    if (totalElement) {

        totalElement.innerText =
            `₹${grandTotal.toFixed(2)}`;

    }

}



// ==========================================
// DISCOUNT LIVE UPDATE
// ==========================================

document.addEventListener("input", function(event) {

    if (event.target.id === "discount") {

        calculateBill();

    }

});



// ==========================================
// PAYMENT METHOD
// ==========================================

function selectPayment(button, method) {

    selectedPayment = method;


    const buttons =
        document.querySelectorAll(".payment-btn");


    buttons.forEach(btn => {

        btn.classList.remove("active");

    });


    button.classList.add("active");

}



// ==========================================
// SEARCH MENU
// ==========================================

document.addEventListener("input", function(event) {

    if (event.target.id !== "menuSearch") {
        return;
    }


    const searchValue =
        event.target.value.toLowerCase().trim();


    const items =
        document.querySelectorAll(".billing-item");


    items.forEach(item => {

        const name =
            item.dataset.name || "";

        const category =
            item.dataset.category || "";


        if (
            name.includes(searchValue) ||
            category.includes(searchValue)
        ) {

            item.style.display = "";

        } else {

            item.style.display = "none";

        }

    });

});



// ==========================================
// CLEAR CART
// ==========================================

function clearCart() {

    if (cart.length === 0) {
        return;
    }


    const confirmed =
        confirm("Are you sure you want to clear this order?");


    if (!confirmed) {
        return;
    }


    cart = [];

    updateCart();

}



// ==========================================
// GENERATE BILL
// ==========================================

function generateBill() {

    if (cart.length === 0) {

        alert(
            "Please add at least one item to the bill."
        );

        return;

    }


    calculateBill();


    const total =
        document.getElementById("grandTotal").innerText;


    alert(
        `Bill generated successfully!\n\n` +
        `Payment: ${selectedPayment}\n` +
        `Total: ${total}`
    );

}



// ==========================================
// PAGE LOAD
// ==========================================

document.addEventListener("DOMContentLoaded", function() {

    console.log(
        "Restaurant Billing System JavaScript Loaded ✅"
    );


    const discount =
        document.getElementById("discount");


    if (discount) {

        discount.addEventListener(
            "input",
            calculateBill
        );

    }

});