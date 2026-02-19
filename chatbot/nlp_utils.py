import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTENTS_PATH = os.path.join(BASE_DIR, "intents.json")

with open(INTENTS_PATH, "r", encoding="utf-8") as file:
    intents = json.load(file)


def extract_data(user_text):
    text = user_text.lower()

    result = {
        "product": None,
        "material": None,
        "budget": None,
        "eco_priority": False
    }

    # Product detection
    for p in intents["products"]:
        if p in text:
            result["product"] = p

    # Material detection
    for m in intents["materials"]:
        if m in text:
            result["material"] = m

    # Budget detection
    for level, words in intents["budget"].items():
        for w in words:
            if w in text:
                result["budget"] = level

    # Eco detection
    for eco in intents["eco_words"]:
        if eco in text:
            result["eco_priority"] = True

    if result["budget"] is None:
        result["budget"] = "medium"

    return result
