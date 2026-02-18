import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_product_image(product, material):
    prompt = f"""
    A realistic eco-friendly {product} made from {material}.
    Modern sustainable product design.
    High quality product rendering, white background.
    """

    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )

        return response["data"][0]["url"]

    except Exception as e:
        print("Image generation error:", e)
        return None
