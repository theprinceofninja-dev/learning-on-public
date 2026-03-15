from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    num1 = float(data["num1"])
    num2 = float(data["num2"])
    operation = data["operation"]

    if operation == "add":
        result = num1 + num2
    elif operation == "subtract":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        if num2 == 0:
            return jsonify({"error": "Division by zero is not allowed"}), 400
        result = num1 / num2
    else:
        return jsonify({"error": "Invalid operation"}), 400

    return jsonify({"result": result})


@app.route("/submit_form", methods=["POST"])
def submit_form():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    if not name or not email:
        return "Name and email are required!", 400

    return f"Thank you {name}! Your message has been received."


if __name__ == "__main__":
    app.run(debug=True)
