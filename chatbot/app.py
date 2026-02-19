import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from chatbot.nlp_utils import extract_data
from sustainability_engine.decision_engine import generate_decision
from image.generator import generate_image

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "EcoDesignAI API is running successfully!"})

@app.route("/design", methods=["POST"])
def design_product():
    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"error": "Please provide product description in 'text' field"}), 400

        user_input = data["text"]

        # STEP 1 — NLP Extraction
        parsed_data = extract_data(user_input)

        product = parsed_data.get("product")
        budget = parsed_data.get("budget")
        eco_priority = parsed_data.get("eco_priority")

        if not product:
            return jsonify({
                "error": "Could not detect product type. Please mention product like bottle, chair, table etc."
            }), 400

        # STEP 2 — Decision Engine
        decision = generate_decision(product, budget, eco_priority)

        # STEP 3 — Image Generation
        recommended_material = decision.get("recommended_material")

        image_url = None

        if recommended_material:
            dss_output = {
                "product": product,
                "material": recommended_material.get("material"),
                "budget": budget,
                "eco_priority": eco_priority,
                "durability": recommended_material.get("durability")
            }

            image_url = generate_image(dss_output)


        # FINAL RESPONSE
        response = {
            "parsed_input": parsed_data,
            "recommended_material": recommended_material,
            "top_3_options": decision.get("top_3_options"),
            "decision_explanation": decision.get("decision_explanation"),
            "image_url": image_url
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
