from flask import Flask, jsonify

app = Flask(__name__)


# Data for user carts
user_carts = {
    1: {"items": [], "total_price": 0.0},
}

# Endpoint to retrieve user's shopping cart
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cart = user_carts.get(user_id, {})
    return jsonify(cart)


# Endpoint to add a product to a user's cart
@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    # Get product information from the Product Service
    # Update the user's shopping cart with the product and quantity
    # Handle errors
    quantity = request.json.get("quantity", 1)
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        user_cart = user_carts.get(user_id)
        if user_cart:
            item = next((i for i in user_cart["items"] if i["product_id"] == product_id), None)
            if item:
                item["quantity"] += quantity
            else:
                new_item = {
                    "product_id": product_id,
                    "product_name": product["name"],
                    "quantity": quantity,
                    "total_price": quantity * product["price"],
                }
                user_cart["items"].append(new_item)
            user_cart["total_price"] += quantity * product["price"]
            return jsonify(user_cart), 200
    return jsonify({"error": "Product or user not found"}), 404

# Endpoint to remove a product from a user's cart
@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    # Remove the specified quantity of the product from the user's cart
    # Handle errors if the product not found or if the quantity exceeds what's in the cart
    quantity = request.json.get("quantity", 1)
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        user_cart = user_carts.get(user_id)
        if user_cart:
            item = next((i for i in user_cart["items"] if i["product_id"] == product_id), None)
            if item:
                if quantity >= item["quantity"]:
                    user_cart["items"].remove(item)
                    user_cart["total_price"] -= item["total_price"]
                else:
                    item["quantity"] -= quantity
                    item["total_price"] -= quantity * product["price"]
                return jsonify(user_cart), 200
    return jsonify({"error": "Product or user not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
