from chatbot.nlp_utils import extract_data
from sustainability_engine.filter_engine import filter_materials

# Simulated User Input
user_text = input("Enter product description: ")

# STEP 1 — Chatbot NLP
chatbot_output = extract_data(user_text)
print("\nChatbot Output:")
print(chatbot_output)

# STEP 2 — Sustainability Engine
materials = filter_materials(
    budget=chatbot_output["budget"],
    eco_priority=chatbot_output["eco_priority"]
)

print("\nSustainability Suggestions:")
for m in materials:
    print(m)
