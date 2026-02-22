MATERIAL_VISUALS = {

    # 🌿 Natural Structural
    "bamboo": "natural bamboo grain, light tan color, visible fiber lines, matte organic surface",
    "wood": "natural wood grain texture, visible growth rings, warm earthy tone",
    "rammed_earth": "compact earth texture, layered soil appearance, matte mineral surface",
    "hempcrete": "lightweight porous surface, chalky mineral texture, natural beige tone",
    "compressed_straw_panel": "compressed straw fibers visible, rough organic texture, warm golden tone",
    "rice_husk_board": "pressed agricultural fiber texture, subtle grainy surface, matte natural finish",
    "bamboo_laminate": "layered bamboo strips, linear grain pattern, smooth semi-matte finish",

    # 🧱 Cement / Composite Structural
    "fly_ash_cement": "fine cement texture with subtle industrial grain, cool gray tone",
    "ferrocement": "dense cement surface with slight roughness, structural industrial finish",

    # 🪵 Plant Fibers (Textile)
    "hemp": "coarse woven natural fiber texture, slightly rough organic fabric",
    "jute": "thick woven plant fiber, rustic rough surface, natural brown tone",
    "linen": "fine woven natural fabric texture, soft matte finish",
    "bamboo_fiber": "smooth plant-based fabric texture, soft woven surface",
    "organic_cotton": "soft woven cotton texture, natural matte fabric folds",
    "recycled_cotton": "woven cotton texture with slight fiber irregularities",
    "silk": "smooth flowing fabric, soft sheen, elegant drape",
    "cork": "speckled cork surface, lightweight porous texture, natural tan color",
    "rubber": "matte flexible surface, slightly elastic texture",
    "fabric": "woven textile surface with natural folds",
    "leather": "natural leather grain texture, subtle surface creases, semi-matte finish",

    # 📦 Paper / Bio Boards
    "cardboard": "layered paperboard texture, visible fiber grain, matte brown surface",
    "paper": "smooth pressed paper surface, matte finish",
    "bagasse_board": "pressed sugarcane fiber texture, subtle organic grain",
    "bioplastic": "smooth molded bioplastic surface, slightly matte eco finish",
    "rice_husk_bioplastic": "smooth bioplastic surface with subtle grain texture",
    "mycelium_composite": "natural organic texture, slightly fibrous surface, matte biodegradable material, light earthy tone",
    
    # 🧪 Plastics
    "plastic": "smooth synthetic plastic surface, uniform texture, semi-gloss finish",
    "recycled_plastic": "smooth molded plastic surface with slight texture variation",

    # 🪨 Rigid Natural
    "ceramic": "smooth glazed ceramic surface, hard solid texture",
    "glass": "clear transparent glass surface, reflective glossy finish",
    "recycled_glass": "translucent glass texture with slight imperfections and bubbles",

    # ⚙️ Metals
    "steel": "brushed steel surface, metallic sheen, cool gray tone",
    "recycled_steel": "brushed recycled steel surface with subtle industrial texture",
    "aluminum": "lightweight brushed aluminum finish, soft metallic sheen",
    "iron": "dark matte iron surface, slightly rough metallic texture",
    "copper": "warm reddish metallic surface, subtle reflective sheen",
    "titanium": "smooth high-strength metallic surface, cool gray metallic finish",
    "carbon_fiber": "woven carbon fiber pattern, high-tech composite texture, subtle gloss",

}






def build_prompt(dss_output):

    product = dss_output["product"].lower()
    material = dss_output["material"].lower()
    budget = dss_output.get("budget", "medium")
    durability = dss_output.get("durability", "medium")
    material_type = dss_output.get("material_type", "rigid")

    # 🔹 Material visual description
    material_visual = MATERIAL_VISUALS.get(
        material,
        f"realistic {material} texture"
    )

    # 🔹 Physical behavior control (VERY IMPORTANT)
    if material_type == "textile":
        structure_hint = (
            "soft flexible structure, natural folds and fabric draping"
        )
    elif material_type == "structural":
        structure_hint = (
            "strong load-bearing solid structure, defined edges and realistic thickness"
        )
    else:  # rigid
        structure_hint = (
            "solid hard structure, defined edges and realistic thickness"
        )

    # 🔹 Product category detection (shape guidance only)
    furniture_products = ["table", "chair", "desk", "sofa"]
    apparel_products = ["shirt", "tshirt", "jacket", "pants"]
    container_products = ["bottle", "cup", "container", "plate"]

    if product in furniture_products:
        product_shape_hint = (
            f"modern {product} furniture with realistic proportions, practical functional design"
        )

    elif product in apparel_products:
        product_shape_hint = (
            f"realistic wearable {product}, ergonomic fit, visible stitching details"
        )

    elif product in container_products:
        product_shape_hint = (
            f"realistic {product} with ergonomic functional shape"
        )

    else:
        product_shape_hint = (
            f"realistic {product} product, practical functional design"
        )

    # 🔹 Structural context (now material-driven behavior)
    structural_context = (
        f"{product_shape_hint}, "
        f"{structure_hint}, "
        f"made of {material}, {material_visual}"
    )

    # 🔹 Core visual style (constant for all)
    style_context = (
        "photorealistic high-end product photography, "
        "studio lighting, white background, soft shadows"
    )

    # 🔹 Quality context
    quality_context = (
        f"{budget} price category, durability level {durability}"
    )

    # 🔹 Eco context
    eco_context = ""
    if dss_output.get("eco_priority"):
        eco_context = (
            ", eco-friendly materials, sustainable design, recyclable components"
        )

    # 🔹 Realism safety guard
    realism_guard = (
        ", realistic object, not abstract, not distorted, not a cube"
    )

    # 🔹 Final prompt assembly
    prompt = (
        f"{style_context}, "
        f"{structural_context}, "
        f"{quality_context}"
        f"{eco_context}"
        f"{realism_guard}"
    )

    return prompt
