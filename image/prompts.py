def build_prompt(dss_output):

    style = "photorealistic product design, minimalist, 3D render, white background"

    eco_features = ""
    if dss_output.get("eco_priority"):
        eco_features = "eco-friendly, recyclable, biodegradable"

    prompt = (
        f"{style}, "
        f"{dss_output['material']} {dss_output['product']}, "
        f"{dss_output['budget']} cost, "
        f"{eco_features}, "
        f"durability {dss_output.get('durability', 'medium')}"
    )

    return prompt
