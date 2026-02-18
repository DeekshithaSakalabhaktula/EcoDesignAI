# test_decision.py
from sustainability_engine.decision_engine import generate_decision

# Example user input
user_input = {
    "product": "bottle",
    "budget": "low",
    "eco_priority": True,
    "durability": "medium"  # optional
}

# Run decision engine
decision = generate_decision(
    product=user_input["product"],
    budget=user_input["budget"],
    eco_priority=user_input["eco_priority"]
)

# Print full result
print("\n--- Decision Output ---")
print(f"Recommended Material: {decision['recommended_material']}")
print(f"Top 3 Options: {decision['top_3_options']}")
print(f"Explanation: {decision['decision_explanation']}")
