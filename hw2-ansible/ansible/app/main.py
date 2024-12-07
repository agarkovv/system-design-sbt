from datetime import datetime

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

visits = 0
messages = []


@app.route("/")
def hello():
    global visits
    visits += 1
    return render_template(
        "index.html", visits=visits, time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


@app.route("/api/status")
def status():
    return jsonify(
        {"status": "healthy", "timestamp": datetime.now().isoformat(), "visits": visits}
    )


@app.route("/message", methods=["POST"])
def add_message():
    content = request.json.get("message", "")
    if content:
        messages.append({"content": content, "timestamp": datetime.now().isoformat()})
        return jsonify({"status": "success"}), 201
    return jsonify({"status": "error", "message": "No message provided"}), 400


@app.route("/messages")
def get_messages():
    return jsonify(messages)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
