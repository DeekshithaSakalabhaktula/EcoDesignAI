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
        "eco_priority": False,
        "durability": None  # FIX #5: added durability field
    }

    # Product detection
    for p in intents["products"]:
        if p in text:
            result["product"] = p

    # FIX #1: Material detection — support partial matches (e.g. "cotton" matches "organic_cotton")
    for m in intents["materials"]:
        readable = m.replace("_", " ")  # "organic_cotton" → "organic cotton"
        # Check exact readable match first, then check if any word in the material name appears
        if readable in text:
            result["material"] = m
            break
        # Partial match: if user types "cotton", match "organic_cotton", "recycled_cotton" etc.
        # We pick the first material whose base word appears in the text
        base_words = readable.split()
        if any(word in text.split() for word in base_words):
            result["material"] = m
            break

    # Budget detection
    for level, words in intents["budget"].items():
        for w in words:
            if w in text:
                result["budget"] = level

    # FIX #2: Eco priority — exclude "organic" alone to avoid false positives from material names
    # Only trigger eco_priority on clearly intentional eco keywords
    eco_words_safe = [e for e in intents["eco_words"] if e != "organic"]
    for eco in eco_words_safe:
        if eco in text:
            result["eco_priority"] = True
            break
    # Allow "organic" only when NOT followed by a material word (i.e. used as a standalone intent)
    if not result["eco_priority"] and "organic" in text:
        # Check that "organic" is not part of a material phrase like "organic cotton"
        material_phrases = [m.replace("_", " ") for m in intents["materials"]]
        if not any("organic" in phrase and phrase in text for phrase in material_phrases):
            result["eco_priority"] = True

    # FIX #5: Durability detection
    for level in ["low", "medium", "high"]:
        if level in text:
            result["durability"] = level
            break

    if result["budget"] is None:
        result["budget"] = "medium"

    return result