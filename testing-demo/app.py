from flask import Flask, jsonify, request

app = Flask(__name__)

# Dữ liệu giả lập trong bộ nhớ
customers = [
    {"id": 1, "name": "Alice", "address": "Hanoi", "phone": "0123456789"},
    {"id": 2, "name": "Bob", "address": "HCM", "phone": "0987654321"}
]

# GET /customers
@app.route('/customers', methods=['GET'])
def get_customers():
    return jsonify(customers), 200

# GET /customers/<id>
@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    for c in customers:
        if c["id"] == customer_id:
            return jsonify(c), 200
    return jsonify({"error": "Customer not found"}), 404

# POST /customers
@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.json
    new_customer = {
        "id": len(customers) + 1,
        "name": data["name"],
        "address": data["address"],
        "phone": data["phone"]
    }
    customers.append(new_customer)
    return jsonify(new_customer), 201

# PUT /customers/<id>
@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    for c in customers:
        if c["id"] == customer_id:
            c.update(request.json)
            return jsonify(c), 200
    return jsonify({"error": "Customer not found"}), 404

# DELETE /customers/<id>
@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    global customers
    customers = [c for c in customers if c["id"] != customer_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5000)
