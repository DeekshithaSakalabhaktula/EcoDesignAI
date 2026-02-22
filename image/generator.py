import os
import uuid
from datetime import datetime
from openai import OpenAI 
from .prompts import build_prompt
from dotenv import load_dotenv
load_dotenv()

# 🔐 Get OpenAI API key
API_KEY = os.getenv("OPENAI_API_KEY")
print("Loaded key starts with:", API_KEY[:10])

if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found. Please set your environment variable.")

client = OpenAI(api_key=API_KEY)

def generate_image(dss_output):
    prompt = build_prompt(dss_output)

    print("Generated Prompt:\n", prompt)

    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_base64 = result.data[0].b64_json

        import base64
        image_bytes = base64.b64decode(image_base64)

        # Create folder if not exists
        output_dir = f"../generated_images/{dss_output['product']}"
        os.makedirs(output_dir, exist_ok=True)

        # Create unique filename
        unique_id = uuid.uuid4().hex[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{dss_output['product']}_{timestamp}_{unique_id}.png"

        filepath = os.path.join(output_dir, filename)

        with open(filepath, "wb") as f:
            f.write(image_bytes)

        print(f"✅ Image saved as {filepath}")
        return filepath.replace("\\", "/")

    except Exception as e:
        print("❌ Image generation error:", str(e))
        return None


# 🔥 TEST BLOCK
if __name__ == "__main__":

    test_dss_output = {
        "product": "table",
        "material": "glass",
        "budget": "high",
        "eco_priority": False,
        "durability": "medium"
    }

    generate_image(test_dss_output)