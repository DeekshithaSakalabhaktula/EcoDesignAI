import os
import uuid
import base64
from datetime import datetime
from openai import OpenAI
from .prompts import build_prompt
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
print("Loaded key starts with:", API_KEY[:10] if API_KEY else "NOT FOUND")

if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found. Please set your environment variable.")

client = OpenAI(api_key=API_KEY)


def generate_image(dss_output):
    """
    Generate a product image via OpenAI gpt-image-1 and save it
    to chatbot/static/generated_images/<product>/.

    dss_output must contain:
        product, material, material_type, budget, eco_priority, durability
    """

    # Validate required fields — fail fast with a clear message
    product = dss_output.get("product")
    material = dss_output.get("material")

    if not product or product == "None":
        print("❌ generate_image: missing product name")
        return None

    if not material or material == "None":
        print("❌ generate_image: missing material name")
        return None

    prompt = build_prompt(dss_output)
    print("Generated Prompt:\n", prompt)

    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_bytes = base64.b64decode(result.data[0].b64_json)

        product_slug = product.lower().replace(" ", "_")

        # Use Flask's static folder so path is always correct regardless of
        # where the server is launched from
        try:
            from flask import current_app
            static_root = current_app.static_folder
        except RuntimeError:
            # Outside app context (e.g. unit tests) — fall back to relative path
            static_root = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "chatbot", "static"
            )

        output_dir = os.path.join(static_root, "generated_images", product_slug)
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:8]
        filename  = f"{product_slug}_{timestamp}_{unique_id}.png"
        filepath  = os.path.join(output_dir, filename)

        with open(filepath, "wb") as f:
            f.write(image_bytes)

        print(f"✅ Image saved: {filepath}")

        # Return the URL path Flask will serve
        return f"/static/generated_images/{product_slug}/{filename}"

    except Exception as e:
        print("❌ Image generation error:", str(e))
        return None


# ── Test block ───────────────────────────────────────────────
if __name__ == "__main__":
    test = {
        "product":      "table",
        "material":     "aluminum",
        "material_type":"structural",
        "budget":       "medium",
        "eco_priority": False,
        "durability":   "high"
    }
    url = generate_image(test)
    print("Result URL:", url)