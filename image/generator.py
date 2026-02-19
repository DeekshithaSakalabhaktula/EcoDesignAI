import requests
import os
from prompts import build_prompt
import uuid
from datetime import datetime



# HuggingFace SDXL Model Endpoint
API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"

# 🔐 Get API Key from environment variable
API_KEY = os.getenv("HF_API_KEY")

if not API_KEY:
    raise ValueError("HF_API_KEY not found. Please set your environment variable.")

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def generate_image(dss_output):
    prompt = build_prompt(dss_output)

    print("Generated Prompt:\n", prompt)

    payload = {
        "inputs": prompt
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
    
       # Create folder if not exists
       output_dir = f"../generated_images/{dss_output['product']}"
       os.makedirs(output_dir, exist_ok=True)

       # Create unique filename
       unique_id = uuid.uuid4().hex[:8]
       timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
       filename = f"{dss_output['product']}_{timestamp}_{unique_id}.png"

       filepath = os.path.join(output_dir, filename)

       with open(filepath, "wb") as f:
           f.write(response.content)

       print(f"✅ Image saved as {filepath}")
       return filepath

    else:
        print("❌ Error:", response.text)
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
