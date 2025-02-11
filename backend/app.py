from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_URL = "http://ollama:11434/api/generate"


def generate_response(prompt):
    data = {
        "model": "deepseek-r1:1.5b",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=data)
        response.raise_for_status()
        return response.json().get("response", "Erro ao gerar resposta.")
    except requests.exceptions.RequestException as e:
        return f"Erro na requisição: {e}"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response_text = generate_response(user_message)
    return jsonify({"response": response_text})

# @app.route("/")
# def home():
#    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
