def calculate_eco_score(row):
    score = 100

    # Carbon impact reduces score
    score -= row["carbon_score"]

    # Non-recyclable penalty
    if row["recyclable"] == "no":
        score -= 20

    # Non-biodegradable penalty
    if row["biodegradable"] == "no":
        score -= 10

    # Low durability penalty
    if row["durability"] == "low":
        score -= 10

    return max(score, 0)
