import json

def load_intents():
    with open("intents.json", "r") as f:
        return json.load(f)

def extract_data(user_text):
    intents = load_intents()
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

    return result
