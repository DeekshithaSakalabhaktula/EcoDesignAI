import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



from flask import Flask, request, jsonify # type: ignore
from nlp_utils import extract_data
from sustainability_engine.filter_engine import filter_materials


app = Flask(__name__)

@app.route("/parse", methods=["POST"])
def parse_text():
    data = request.get_json()
    user_input = data.get("text", "")

    # Step 1: NLP extraction
    result = extract_data(user_input)

    # Step 2: Get parameters
    budget = result.get("budget")
    eco_priority = result.get("eco_priority")

    # Step 3: Call sustainability engine
    materials = filter_materials(budget, eco_priority)

    # Step 4: Add top 3 materials to response
    result["recommended_materials"] = materials[:3]

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
