import os
import json
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTENTS_PATH = os.path.join(BASE_DIR, "intents.json")

with open(INTENTS_PATH, "r", encoding="utf-8") as file:
    intents = json.load(file)

# Pre-sort materials longest-first so "bamboo_laminate" matches before "bamboo"
_sorted_materials = sorted(intents["materials"], key=lambda m: len(m), reverse=True)


def extract_data(user_text, expected_slot=None):
    text = user_text.lower().strip()

    result = {
        "product":      None,
        "material":     None,
        "budget":       None,
        "eco_priority": None,
        "durability":   None
    }

    # ── Product ──────────────────────────────────────────────
    if expected_slot in [None, "product"]:
        for p in intents["products"]:
            # whole-word match to avoid "shirt" matching "t-shirt" wrong
            if re.search(r'\b' + re.escape(p) + r'\b', text):
                result["product"] = p
                break

    # ── Material ─────────────────────────────────────────────
    # Longest-first prevents "hemp" stealing "hempcrete"
    if expected_slot in [None, "material"]:
        for m in _sorted_materials:
            readable = m.replace("_", " ")
            # Full phrase match first (e.g. "bamboo laminate")
            if re.search(r'\b' + re.escape(readable) + r'\b', text):
                result["material"] = m
                break

    # ── Budget ───────────────────────────────────────────────
    if expected_slot in [None, "budget"]:
        for level, words in intents["budget"].items():
            for w in words:
                if re.search(r'\b' + re.escape(w) + r'\b', text):
                    result["budget"] = level
                    break
            if result["budget"]:
                break

    # ── Eco priority ─────────────────────────────────────────
    if expected_slot in [None, "eco_priority"]:
        eco_words_safe = [e for e in intents["eco_words"] if e != "organic"]

        for eco in eco_words_safe:
            if re.search(r'\b' + re.escape(eco) + r'\b', text):
                result["eco_priority"] = eco
                break

        if result["eco_priority"] is None and "organic" in text:
            material_phrases = [m.replace("_", " ") for m in intents["materials"]]
            is_material_context = any(
                "organic" in phrase and re.search(r'\b' + re.escape(phrase) + r'\b', text)
                for phrase in material_phrases
            )
            if not is_material_context:
                result["eco_priority"] = "organic"

    # ── Durability ───────────────────────────────────────────
    if expected_slot in [None, "durability"]:
        for level in ["high", "medium", "low"]:
            if re.search(r'\b' + level + r'\b', text):
                result["durability"] = level
                break

    return result