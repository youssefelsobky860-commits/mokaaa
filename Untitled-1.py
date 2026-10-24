from flask import Flask, jsonify, render_template, request, session
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)


def start_game():
    session["number"] = secrets.randbelow(100) + 1
    session["attempts"] = 0


@app.get("/")
def index():
    if "number" not in session:
        start_game()
    return render_template("index.html")


@app.post("/guess")
def guess():
    try:
        value = int(request.json.get("guess"))
    except (ValueError, TypeError, AttributeError):
        return jsonify(message="اكتب رقمًا صحيحًا من 1 إلى 100.")

    if not 1 <= value <= 100:
        return jsonify(message="الرقم يجب أن يكون بين 1 و100.")

    session["attempts"] += 1
    target = session["number"]

    if value < target:
        return jsonify(message="جرّب رقمًا أكبر ↑")

    if value > target:
        return jsonify(message="جرّب رقمًا أصغر ↓")

    attempts = session["attempts"]
    start_game()
    return jsonify(message=f"أحسنت! فزت في {attempts} محاولات 🎉")


if __name__ == "__main__":
    app.run(debug=True)