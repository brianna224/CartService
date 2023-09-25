# Brianna Patrick CMSC455   
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

PRODUCT_SERVICE_URL = "https://product-service-faid.onrender.com"
#PRODUCT_SERVICE_URL = "http://127.0.0.1:5000"

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
    response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")

    if response.status_code == 200:
        product_data = response.json()
        quantity = request.json.get("quantity", 1)
        # change quantity to equal the user specified quantity
        user_cart = user_carts.get(user_id)
        if user_cart:
            item = next((i for i in user_cart["items"] if i["product_id"] == product_id), None)
            if item:
                item["quantity"] += quantity
                item["total_price"] += quantity * product_data["price"]
            else:
                new_item = {
                    "product_id": product_id,
                    "product_name": product_data["name"],
                    "quantity": quantity,
                    "total_price": quantity * product_data["price"],
                }
                user_cart["items"].append(new_item)
            user_cart["total_price"] += quantity * product_data["price"]
            return jsonify(user_cart), 200
    else:
        return jsonify({"error": "Product not found"}), 404

# Endpoint to remove a product from a user's cart
@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    # Remove the specified quantity of the product from the user's cart
    # Handle errors if the product not found or if the quantity exceeds what's in the cart
    response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")

    if response.status_code == 200:
        product_data = response.json()
        quantity = request.json.get("quantity", 1)
        user_cart = user_carts.get(user_id)
        if user_cart:
            item = next((i for i in user_cart["items"] if i["product_id"] == product_id), None)
            if item:
                if quantity >= item["quantity"]:
                    user_cart["items"].remove(item)
                    user_cart["total_price"] -= item["total_price"]
                else:
                    item["quantity"] -= quantity
                    item["total_price"] -= quantity * product_data["price"]
                return jsonify(user_cart), 200
    else:
        return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    #app.run(debug=True, port=6000)
