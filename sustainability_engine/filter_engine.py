from .sustainability_db import load_materials
from .eco_score import calculate_eco_score


def filter_materials(budget=None, eco_priority=False):
    df = load_materials()

    if df is None:
        return []

    # Budget Filtering
    if budget:
        df = df[df["cost_level"] == budget]

    # If eco_priority is True, remove high carbon materials
    if eco_priority:
        df = df[df["carbon_score"] <= 40]

    # Calculate Eco Score
    df["eco_score"] = df.apply(calculate_eco_score, axis=1)

    # Sort by best eco_score
    df = df.sort_values(by="eco_score", ascending=False)

    return df.to_dict(orient="records")
