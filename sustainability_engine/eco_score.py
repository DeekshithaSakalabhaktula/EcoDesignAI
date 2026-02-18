def calculate_eco_score(row):
    try:
        score = 100

        carbon = float(row["carbon_score"])
        score -= carbon

        if str(row["recyclable"]).lower() == "no":
            score -= 20

        if str(row["biodegradable"]).lower() == "no":
            score -= 10

        if str(row["durability"]).lower() == "low":
            score -= 10

        return max(score, 0)

    except Exception as e:
        print("Eco score error:", e)
        return 0
