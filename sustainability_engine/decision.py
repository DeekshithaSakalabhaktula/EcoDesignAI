from .filter_engine import filter_materials

def generate_decision(product=None, budget=None, eco_priority=False):
    materials = filter_materials(budget, eco_priority)

    if not materials:
        return {
            "product": product,
            "message": "No suitable materials found.",
            "recommendations": []
        }

    top_material = materials[0]

    explanation = f"""
For designing a {product}, the best material is {top_material['material']}.

Reason:
- Carbon Score: {top_material['carbon_score']}
- Recyclable: {top_material['recyclable']}
- Biodegradable: {top_material['biodegradable']}
- Durability: {top_material['durability']}
- Overall Eco Score: {top_material['eco_score']}

This material satisfies the selected budget and sustainability preferences.
"""

    return {
        "product": product,
        "recommended_material": top_material,
        "top_3_options": materials[:3],
        "decision_explanation": explanation.strip()
    }
