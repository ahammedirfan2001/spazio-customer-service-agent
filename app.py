from flask import Flask, render_template, request, jsonify
from agent import chat_with_agent

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}

    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please enter a message."}), 400

    try:
        reply = chat_with_agent(user_message)
        return jsonify({"reply": reply})

    except Exception as error:
        app.logger.exception("Error while processing chat message")
        return jsonify({
            "reply": "Sorry, something went wrong. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)