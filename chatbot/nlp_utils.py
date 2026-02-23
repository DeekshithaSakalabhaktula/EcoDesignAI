import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTENTS_PATH = os.path.join(BASE_DIR, "intents.json")

with open(INTENTS_PATH, "r", encoding="utf-8") as file:
    intents = json.load(file)


def extract_data(user_text, expected_slot=None):
    text = user_text.lower()

    result = {
        "product": None,
        "material": None,
        "budget": None,
        "eco_priority": None,
        "durability": None
    }

    # -----------------------------
    # Product Detection
    # -----------------------------
    if expected_slot in [None, "product"]:
        for p in intents["products"]:
            normalized_product = p.replace(" ", "")
            normalized_text = text.replace(" ", "")
            if p in text or normalized_product in normalized_text:
                result["product"] = p
                break

    # -----------------------------
    # Material Detection
    # -----------------------------
    if expected_slot in [None, "material"]:
        for m in intents["materials"]:
            readable = m.replace("_", " ")
            if readable in text:
                result["material"] = m
                break

            base_words = readable.split()
            if any(word in text.split() for word in base_words):
                result["material"] = m
                break

    # -----------------------------
    # Budget Detection
    # -----------------------------
    if expected_slot in [None, "budget"]:
        for level, words in intents["budget"].items():
            for w in words:
                if w in text:
                    result["budget"] = level
                    break
            if result["budget"]:
                break

    # -----------------------------
    # Eco Priority Detection
    # -----------------------------
    if expected_slot in [None, "eco_priority"]:
        eco_words_safe = [e for e in intents["eco_words"] if e != "organic"]

        for eco in eco_words_safe:
            if eco in text:
                result["eco_priority"] = eco
                break

        if result["eco_priority"] is None and "organic" in text:
            material_phrases = [m.replace("_", " ") for m in intents["materials"]]
            if not any("organic" in phrase and phrase in text for phrase in material_phrases):
                result["eco_priority"] = "organic"

    # -----------------------------
    # Durability Detection
    # -----------------------------
    if expected_slot in [None, "durability"]:
        for level in ["low", "medium", "high"]:
            if level in text:
                result["durability"] = level
                break

    return result