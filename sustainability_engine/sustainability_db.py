import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "materials.csv")

def load_materials():
    try:
        df = pd.read_csv(CSV_PATH)
        return df
    except Exception as e:
        print("Error loading materials:", e)
        return None
