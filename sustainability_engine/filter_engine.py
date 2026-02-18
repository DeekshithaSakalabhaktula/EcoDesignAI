from .sustainability_db import load_materials
from .eco_score import calculate_eco_score

def filter_materials(budget=None, eco_priority=False):
    df = load_materials()

    if df is None or df.empty:
        return []

    # Budget filter
    if budget:
        df = df[df["cost_level"] == budget]

    # Eco filter
    if eco_priority:
        df = df[df["carbon_score"] <= 40]

    if df.empty:
        return []

    # Add eco score
    df["eco_score"] = df.apply(calculate_eco_score, axis=1)

    # Sort
    df = df.sort_values(by="eco_score", ascending=False)

    # Convert safely
    records = df.to_dict(orient="records")

    return records
