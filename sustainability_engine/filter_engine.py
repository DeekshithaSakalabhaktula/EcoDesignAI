from .sustainability_db import load_materials
from .eco_score import calculate_eco_score

def filter_materials(budget=None, eco_priority=False, min_durability=None):
    df = load_materials()

    if df is None or df.empty:
        return []

    # Budget filter
    if budget:
        if "cost_level" in df.columns:
            df = df[df["cost_level"] == budget]
        

    # Eco filter
    if eco_priority:
        if "carbon_score" in df.columns and "material" in df.columns:
            df = df[(df["carbon_score"] <= 40) & (df["material"].str.lower() != "plastic")]

     # Durability filter
    if min_durability and "durability" in df.columns:
        allowed = ["medium", "high"]  # example threshold
        if min_durability.lower() == "high":
            allowed = ["high"]
        df = df[df["durability"].isin(allowed)]

    if df.empty:
        return []

    # Add eco score
    df["eco_score"] = df.apply(calculate_eco_score, axis=1)

    # Sort
    df = df.sort_values(by="eco_score", ascending=False)

    # Convert safely
    records = df.to_dict(orient="records")

    return records
