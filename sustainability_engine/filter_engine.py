from .sustainability_db import load_materials
from .eco_score import calculate_eco_score


PRODUCT_MATERIAL_MAP = {

    # TEXTILE
    "shirt": "textile",
    "tshirt": "textile",
    "jacket": "textile",
    "pants": "textile",
    "clothes": "textile",
    "bag": "textile",
    "backpack": "textile",
    "shoe": "textile",

    # STRUCTURAL / FURNITURE
    "chair": "structural",
    "table": "structural",
    "sofa": "structural",
    "desk": "structural",
    "shelf": "structural",
    "bed": "structural",
    "cabinet": "structural",
    "stool": "structural",
    "stand": "structural",
    "rack": "structural",

    # RIGID / HARD GOODS
    "bottle": "rigid",
    "cup": "rigid",
    "box": "rigid",
    "phone case": "rigid",
    "lamp": "rigid",
    "planter": "rigid",
    "notebook": "rigid",
    "helmet": "rigid",
    "bowl": "rigid",
    "plate": "rigid",
    "watch": "rigid"
}


def filter_materials(product=None, budget=None, eco_priority=False, min_durability=None):

    df = load_materials()

    if df is None or df.empty:
        return []

    df = df.copy()

    # -------------------
    # Product compatibility filter
    # -------------------
    if product:
        product = product.strip().lower()

        if product in PRODUCT_MATERIAL_MAP:
            required_type = PRODUCT_MATERIAL_MAP[product]

            if "material_type" in df.columns:
                df = df[df["material_type"].str.lower() == required_type.lower()]

    # -------------------
    # Budget filter
    # -------------------
    if budget and "cost_level" in df.columns:
        df = df[df["cost_level"].str.lower() == str(budget).lower()]

    # -------------------
    # Eco filter
    # -------------------
    if eco_priority and "carbon_score" in df.columns:
        df = df[df["carbon_score"] <= 50]

    # -------------------
    # Durability filter
    # -------------------
    if min_durability and "durability" in df.columns:
        df = df[df["durability"].str.lower() == min_durability.lower()]

    if df.empty:
        return []

    # -------------------
    # Add eco score
    # -------------------
    df["eco_score"] = df.apply(calculate_eco_score, axis=1)

    # -------------------
    # Sort
    # -------------------
    df = df.sort_values(by="eco_score", ascending=False)

    return df.to_dict(orient="records")