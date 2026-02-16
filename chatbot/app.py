from flask import Flask, request, jsonify # type: ignore
from nlp_utils import extract_data

app = Flask(__name__)

@app.route("/parse", methods=["POST"])
def parse_text():
    data = request.get_json()
    user_input = data.get("text", "")
    result = extract_data(user_input)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
