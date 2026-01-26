from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage (for demo)
calculation = {
    "a": 0,
    "b": 0,
    "operation": "add",
    "result": 0
}


def calculate(a, b, operation):
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            return "Division by zero not allowed"
        return a / b
    else:
        return "Invalid operation"


@app.route("/calculate", methods=["GET", "POST", "PUT", "PATCH"])
def math_api():

    global calculation

    # ✅ GET → Read calculation
    if request.method == "GET":
        return jsonify(calculation)

    data = request.get_json()

    # ✅ POST → Create new calculation
    if request.method == "POST":
        calculation = {
            "a": data["a"],
            "b": data["b"],
            "operation": data["operation"]
        }
        calculation["result"] = calculate(
            calculation["a"],
            calculation["b"],
            calculation["operation"]
        )
        return jsonify(calculation), 201

    # ✅ PUT → Full update (all fields required)
    if request.method == "PUT":
        calculation["a"] = data["a"]
        calculation["b"] = data["b"]
        calculation["operation"] = data["operation"]
        calculation["result"] = calculate(
            calculation["a"],
            calculation["b"],
            calculation["operation"]
        )
        return jsonify(calculation)

    # ✅ PATCH → Partial update
    if request.method == "PATCH":
        calculation["a"] = data.get("a", calculation["a"])
        calculation["b"] = data.get("b", calculation["b"])
        calculation["operation"] = data.get(
            "operation", calculation["operation"]
        )
        calculation["result"] = calculate(
            calculation["a"],
            calculation["b"],
            calculation["operation"]
        )
        return jsonify(calculation)


if __name__ == "__main__":
    app.run(debug=True)



