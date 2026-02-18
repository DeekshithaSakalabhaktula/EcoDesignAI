from .filter_engine import filter_materials

def generate_decision(product=None, budget=None, eco_priority=False):
    materials = filter_materials(budget, eco_priority)

    if not materials:
        return {
            "product": product,
            "recommended_material": None,
            "top_3_options": [],
            "decision_explanation": "No suitable materials found."
        }

    top_material = materials[0]

    explanation = f"""
For designing a {product}, the best material is {top_material.get('material')}.

Reason:
- Carbon Score: {top_material.get('carbon_score')}
- Recyclable: {top_material.get('recyclable')}
- Biodegradable: {top_material.get('biodegradable')}
- Durability: {top_material.get('durability')}
- Overall Eco Score: {top_material.get('eco_score')}

This material satisfies the selected budget and sustainability preferences.
"""

    return {
        "product": product,
        "recommended_material": top_material,
        "top_3_options": materials[:3],
        "decision_explanation": explanation.strip()
    }
