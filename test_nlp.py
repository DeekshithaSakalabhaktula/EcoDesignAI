import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chatbot.nlp_utils import extract_data


def test_nlp_extraction():
    test_sentences = [
        "I want a low budget eco-friendly table",
        "Suggest a sustainable chair with medium budget",
        "High eco priority wooden desk"
    ]

    for sentence in test_sentences:
        print("\nInput:", sentence)
        result = extract_data(sentence)
        print("Extracted Output:", result)


if __name__ == "__main__":
    test_nlp_extraction()