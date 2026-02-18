from chatbot.nlp_utils import extract_data
from sustainability_engine.decision_engine import generate_decision

def main():
    # STEP 0 — User Input
    user_text = input("Enter product description: ")

    # STEP 1 — NLP Extraction
    parsed_data = extract_data(user_text)

    print("\n🔎 Chatbot NLP Output:")
    print(parsed_data)

    # Extract parameters
    product = parsed_data.get("product")
    budget = parsed_data.get("budget")
    eco_priority = parsed_data.get("eco_priority")

    # STEP 2 — Decision Engine
    decision = generate_decision(product, budget, eco_priority)

    print("\n🧠 Decision Engine Output:")
    print("\nRecommended Material:")
    print(decision.get("recommended_material"))

    print("\nTop 3 Options:")
    for material in decision.get("top_3_options", []):
        print(material)

    print("\nExplanation:")
    print(decision.get("decision_explanation"))

if __name__ == "__main__":
    main()
