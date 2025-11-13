from flask import Flask, request, jsonify

app = Flask(__name__)

# ========== API V1 ==========
@app.route("/api/v1/payments", methods=["POST"])
def create_payment_v1():
    """
    Version 1: nhận amount và currency qua query param
    """
    amount = request.args.get("amount", type=float)
    currency = request.args.get("currency", default="USD", type=str)

    if amount is None:
        return jsonify({"error": "Missing amount"}), 400

    return jsonify({
        "message": f"✅ [v1] Payment created: {amount} {currency}",
        "deprecated": True,
        "notice": "API v1 sẽ ngừng hoạt động sau 31/12/2025. Hãy dùng /api/v2/payments"
    })


@app.route("/api/v1/payments/notice", methods=["GET"])
def deprecation_notice():
    message = {
        "warning": "⚠️ API v1 sẽ bị ngừng hoạt động sau 31/12/2025.",
        "action": "Vui lòng chuyển sang /api/v2/payments để dùng phiên bản mới.",
        "migration_guide": "https://example.com/api-migration-guide"
    }
    return jsonify(message)


# ========== API V2 ==========
@app.route("/api/v2/payments", methods=["POST"])
def create_payment_v2():
    """
    Version 2: Nhận dữ liệu JSON (breaking change)
    {
      "amount": 100,
      "currency": "USD",
      "method": "credit_card"
    }
    """
    data = request.get_json(silent=True)
    if not data or "amount" not in data or "method" not in data:
        return jsonify({
            "error": "Invalid JSON. Required fields: amount, currency, method"
        }), 400

    amount = data["amount"]
    currency = data.get("currency", "USD")
    method = data["method"]

    return jsonify({
        "message": f"✅ [v2] Payment created using {method} ({amount} {currency})",
        "version": "2.0",
        "status": "success"
    })


if __name__ == "__main__":
    app.run(debug=True)
