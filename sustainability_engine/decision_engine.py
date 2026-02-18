from .filter_engine import filter_materials

def generate_decision(product=None, budget=None, eco_priority=False, durability_req=None):
    materials = filter_materials(budget=budget, eco_priority=eco_priority, min_durability=durability_req)

    if not materials:
        return {
            "product": product,
            "recommended_material": None,
            "top_3_options": [],
            "decision_explanation": "No suitable materials found."
        }

    top_material = materials[0]

    explanation = (
        f"For designing a {product}, the best material is "
        f"{top_material.get('material')}.\n"
        f"Reason:\n"
        f"  • Carbon Score: {top_material.get('carbon_score')}\n"
        f"  • Recyclable: {top_material.get('recyclable')}\n"
        f"  • Biodegradable: {top_material.get('biodegradable')}\n"
        f"  • Durability: {top_material.get('durability')}\n"
        f"  • Eco Score: {top_material.get('eco_score')}\n"
        "This material satisfies selected budget and sustainability preferences."
)


    return {
        "product": product,
        "recommended_material": top_material,
        "top_3_options": materials[:3],
        "decision_explanation": explanation.strip()
    }
