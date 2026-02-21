import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify # type: ignore
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
        print("Parsed Data:", parsed_data)

        product = parsed_data.get("product")
        budget = parsed_data.get("budget")
        eco_priority = parsed_data.get("eco_priority")
        preferred_material = parsed_data.get("material")
        durability_req = parsed_data.get("durability")  # FIX #5: now correctly populated by extract_data

        if not product:
            return jsonify({
                "error": "Could not detect product type. Please mention product like bottle, chair, table etc."
            }), 400

        # STEP 2 — Decision Engine
        decision = generate_decision(
            product=product,
            budget=budget,
            eco_priority=eco_priority,
            durability_req=durability_req,
            preferred_material=preferred_material
        )
        print("Decision:", decision)

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

        # FINAL RESPONSE — FIX #4: product key now included via decision dict
        response = {
            "parsed_input": parsed_data,  # FIX #5: durability now present here
            "product": decision.get("product"),  # FIX #4: explicitly expose product
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