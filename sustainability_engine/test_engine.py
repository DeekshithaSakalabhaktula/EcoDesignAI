from decision_engine import generate_decision

result = generate_decision(
    product="shirt",
    budget="low",
    eco_priority=True,
    durability_req="medium"
)

print("\n===== RECOMMENDATION RESULT =====\n")

if result["recommended_material"]:
    print("Recommended Material:", result["recommended_material"]["material"])
    print("\nTop 3 Options:")
    for item in result["top_3_options"]:
        print("-", item["material"])

    print("\nExplanation:\n")
    print(result["decision_explanation"])
else:
    print(result["decision_explanation"])