def build_prompt(dss_output):

    parts = []

    parts.append("photorealistic product design")
    parts.append("minimalist")
    parts.append("3D render")
    parts.append("white background")

    parts.append(f"{dss_output['material']} {dss_output['product']}")
    parts.append(f"{dss_output['budget']} cost")

    if dss_output.get("eco_priority"):
        parts.append("eco-friendly")
        parts.append("recyclable")
        parts.append("biodegradable")

    parts.append(f"durability {dss_output.get('durability', 'medium')}")

    return ", ".join(parts)