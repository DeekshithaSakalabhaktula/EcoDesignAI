from .sustainability_db import load_materials
from .eco_score import calculate_eco_score


PRODUCT_MATERIAL_MAP = {

    # TEXTILE
    "shirt": "textile",
    "tshirt": "textile",
    "t-shirt": "textile",   # FIX #7: added hyphenated variant
    "t shirt": "textile",   # FIX #7: added spaced variant
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


# -------------------------
# Mapping helpers
# -------------------------

def map_durability(value):
    mapping = {"low": 1, "medium": 2, "high": 3}
    return mapping.get(str(value).lower(), 1)


def map_cost(value):
    # Lower cost = better sustainability score
    mapping = {"low": 3, "medium": 2, "high": 1}
    return mapping.get(str(value).lower(), 1)


# -------------------------
# Final Sustainability Score
# -------------------------

def calculate_final_score(row, eco_priority=False):
    eco_weight = 0.5 if eco_priority else 0.3
    durability_weight = 0.3
    cost_weight = 0.2

    eco_component = row["eco_score"] * eco_weight
    durability_component = map_durability(row.get("durability")) * 10 * durability_weight
    cost_component = map_cost(row.get("cost_level")) * 10 * cost_weight

    return eco_component + durability_component + cost_component


# -------------------------
# Main Filter Function
# -------------------------

def filter_materials(product=None, budget=None, eco_priority=False, min_durability=None, preferred_material=None):

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
    # Durability filter
    # -------------------
    if min_durability and "durability" in df.columns:
        df = df[df["durability"].str.lower() == min_durability.lower()]

    if df.empty:
        return []

    # -------------------
    # Preferred material filter (partial match)
    # -------------------
    if preferred_material:
        preferred_material = preferred_material.lower().strip().replace("_", " ")  # normalize underscores
        # Normalize the material column too before matching
        df["preferred"] = df["material"].str.lower().str.replace("_", " ").str.contains(preferred_material)
    else:
        df["preferred"] = False

    # -------------------
    # Calculate eco score
    # -------------------
    df["eco_score"] = df.apply(calculate_eco_score, axis=1)

    # -------------------
    # Calculate final composite score
    # -------------------
    df["final_score"] = df.apply(
        lambda row: calculate_final_score(row, eco_priority),
        axis=1
    )

    # FIX #3: Removed duplicate sort_values call — only one sort needed
    df = df.sort_values(by=["preferred", "final_score"], ascending=[False, False])

    return df.to_dict(orient="records")