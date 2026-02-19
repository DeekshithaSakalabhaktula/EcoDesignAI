from .filter_engine import filter_materials


def interpret_carbon(score):
    if score <= 30:
        return "Low carbon impact"
    elif score <= 60:
        return "Moderate carbon impact"
    else:
        return "High carbon impact"


def interpret_durability(score):
    if score >= 8:
        return "Highly durable"
    elif score >= 5:
        return "Moderately durable"
    else:
        return "Low durability"


def generate_decision(product=None, budget=None, eco_priority=False, durability_req=None):


    # Convert budget string to numeric level
    budget_map = {
         "low": 1,
         "medium": 2,
         "high": 4
    }

    if isinstance(budget, str):
        budget = budget_map.get(budget.lower(), 2)

    materials = filter_materials(
        budget=budget,
        eco_priority=eco_priority,
        min_durability=durability_req
    )

    if not materials:
        return {
            "product": product,
            "recommended_material": None,
            "top_3_options": [],
            "decision_explanation": "No suitable materials found based on selected constraints."
        }

    top_material = materials[0]
    second_material = materials[1] if len(materials) > 1 else None

    carbon_meaning = interpret_carbon(top_material.get("carbon_score", 0))
    durability_meaning = interpret_durability(top_material.get("durability", 0))

    explanation = (
        f"For designing a {product}, the most suitable material is "
        f"{top_material.get('material')}.\n\n"
        f"Sustainability Profile:\n"
        f"• Carbon Score: {top_material.get('carbon_score')} ({carbon_meaning})\n"
        f"• Eco Score: {top_material.get('eco_score')}\n"
        f"• Recyclable: {top_material.get('recyclable')}\n"
        f"• Biodegradable: {top_material.get('biodegradable')}\n"
        f"• Durability: {top_material.get('durability')} ({durability_meaning})\n\n"
    )

    if second_material:
        explanation += (
            f"Comparison Insight:\n"
            f"Compared to {second_material.get('material')}, "
            f"{top_material.get('material')} provides a better balance between "
            f"sustainability and durability while fitting within your selected budget.\n\n"
        )

    explanation += (
        "This recommendation aligns with your budget preferences and "
        "sustainability priority settings, offering an optimal eco-conscious design choice."
    )

    return {
        "product": product,
        "recommended_material": top_material,
        "top_3_options": materials[:3],
        "decision_explanation": explanation.strip()
    }
