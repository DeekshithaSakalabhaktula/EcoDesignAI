import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify, render_template
from chatbot.nlp_utils import extract_data
from sustainability_engine.decision_engine import generate_decision
from image.generator import generate_image



# ---------------------------------
# Conversation State (Memory)
# ---------------------------------

conversation_state = {
    "product": None,
    "material": None,
    "budget": None,
    "eco_priority": None,
    "durability": None,
    "awaiting": None,
    "material_options": None
}


# ---------------------------------
# Helper Functions
# ---------------------------------

def update_conversation_state(parsed_data):
    for key in conversation_state:
        if parsed_data.get(key):
            conversation_state[key] = parsed_data.get(key)


def check_missing_slots():
    missing = []

    if conversation_state["product"] is None:
        missing.append("product")

    if conversation_state["budget"] is None:
        missing.append("budget")

    if conversation_state["eco_priority"] is None:
        missing.append("eco_priority")

    return missing


def reset_conversation():
    for key in conversation_state:
        conversation_state[key] = None


MATERIAL_DATA = {
    "plastic": {
        "carbon": 8,
        "recyclable": "Partial",
        "cost": "Low",
        "durability": "High"
    },
    "bamboo": {
        "carbon": 2,
        "recyclable": "Yes",
        "cost": "Low",
        "durability": "Medium"
    },
    "steel": {
        "carbon": 6,
        "recyclable": "Yes",
        "cost": "Medium",
        "durability": "High"
    },
    "aluminum": {
        "carbon": 3,
        "recyclable": "Yes",
        "cost": "Medium",
        "durability": "High"
    }
}



# ---------------------------------
# Flask App
# ---------------------------------

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"message": "EcoDesignAI API is running successfully!"})


@app.route("/design", methods=["POST"])
def design_product():
    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({
                "error": "Please provide product description in 'text' field"
            }), 400

        user_input = data["text"]

        # STEP 1 — NLP Extraction
        parsed_data = extract_data(
            user_input,
            expected_slot=conversation_state.get("awaiting")
        )

        print("Parsed Data:", parsed_data)

        # STEP 2 — Update Memory
        update_conversation_state(parsed_data)

        # ---------------------------------
        # STEP 3 — If waiting for material selection
        # ---------------------------------
        if conversation_state.get("awaiting") == "material_selection":

            user_text_lower = user_input.lower()
            selected_material = None
            for option in conversation_state.get("material_options", []):
                if option["material"].lower() in user_text_lower:
                    selected_material = option["material"]
                    break

            # CASE 1 — User selects material explicitly
            if selected_material:
                conversation_state["material"] = selected_material
                conversation_state["awaiting"] = None

            # CASE 2 — User asks for best recommendation
            elif any(word in user_text_lower for word in [
                "best", "recommend", "suggest", "you choose", "your choice"
            ]):
                best_option = conversation_state["material_options"][0]
                conversation_state["material"] = best_option["material"]
                conversation_state["awaiting"] = None

            # CASE 3 — Invalid reply
            else:
                return jsonify({
                    "clarification": "Please select one of the suggested materials or say 'recommend best'.",
                    "options": conversation_state.get("material_options"),
                    "current_state": conversation_state
                })

            # ---------------------------------
            # Generate Decision First (Explain)
            # ---------------------------------
            decision = generate_decision(
                product=conversation_state["product"],
                budget=conversation_state["budget"],
                eco_priority=conversation_state["eco_priority"],
                durability_req=conversation_state["durability"],
                preferred_material=conversation_state["material"]
            )

            recommended_material = decision.get("recommended_material")

            # ---------------------------------
            # Generate Image AFTER explanation
            # ---------------------------------
            image_url = None
            if recommended_material:
                dss_output = {
                    "product": decision.get("product"),
                    "material": recommended_material.get("material"),
                    "budget": conversation_state["budget"],
                    "eco_priority": conversation_state["eco_priority"],
                    "durability": recommended_material.get("durability")
                }

                image_url = generate_image(dss_output)

            response = {
                "message": f"For your {decision.get('product')}, I recommend {recommended_material.get('material')} as the best eco-friendly option.",
                "decision_explanation": decision.get("decision_explanation"),
                "recommended_material": recommended_material,
                "image_url": image_url
            }

            reset_conversation()
            return jsonify(response)

        # ---------------------------------
        # STEP 4 — Check missing required slots
        # ---------------------------------
        missing_fields = check_missing_slots()

        if missing_fields:

            if "product" in missing_fields:
                conversation_state["awaiting"] = "product"
                return jsonify({
                    "clarification": "What product would you like to design? (Bottle, Chair, Table, Shirt etc.)",
                    "current_state": conversation_state
                })

            if "budget" in missing_fields:
                conversation_state["awaiting"] = "budget"
                return jsonify({
                    "clarification": "What is your budget range? (Low, Medium, High)",
                    "current_state": conversation_state
                })

            if "eco_priority" in missing_fields:
                conversation_state["awaiting"] = "eco_priority"
                return jsonify({
                    "clarification": "What is your eco priority? (Low Carbon, Biodegradable, Recyclable)",
                    "current_state": conversation_state
                })

        # ---------------------------------
        # STEP 5 — Generate decision
        # ---------------------------------
        decision = generate_decision(
            product=conversation_state["product"],
            budget=conversation_state["budget"],
            eco_priority=conversation_state["eco_priority"],
            durability_req=conversation_state["durability"],
            preferred_material=conversation_state["material"]
        )

        top_3 = decision.get("top_3_options")

        # If no material selected → ask user to choose
        if conversation_state["material"] is None and top_3:

            conversation_state["awaiting"] = "material_selection"
            conversation_state["material_options"] = top_3

            return jsonify({
                "clarification": "Here are the top eco-friendly material options. Please choose one or say 'recommend best':",
                "options": top_3,
                "current_state": conversation_state
            })

        # Otherwise generate image immediately
        recommended_material = decision.get("recommended_material")

        image_url = None
        if recommended_material:
            dss_output = {
                "product": conversation_state["product"],
                "material": recommended_material.get("material"),
                "budget": conversation_state["budget"],
                "eco_priority": conversation_state["eco_priority"],
                "durability": recommended_material.get("durability")
            }

            image_url = generate_image(dss_output)

        response = {
            "final_recommendation": {
                "product": decision.get("product"),
                "recommended_material": recommended_material,
                "top_3_options": decision.get("top_3_options"),
                "decision_explanation": decision.get("decision_explanation")
            },
            "image_url": image_url
        }

        reset_conversation()
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/studio")
def studio():
    return render_template("studio.html")

@app.route("/api/material/<name>")
def get_material(name):
    return jsonify(MATERIAL_DATA.get(name, {}))

@app.route("/api/send_to_chatbot", methods=["POST"])
def send_to_chatbot():
    data = request.json
    message = data["message"]

    # You can connect this to your existing chatbot logic
    print("Sending to chatbot:", message)

    return jsonify({"status": "sent"})

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

if __name__ == "__main__":
    app.run(debug=True)