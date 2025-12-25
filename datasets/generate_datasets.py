import os
import json
import random

DATASET_DIR = "datasets/generated"
NUM_DATASETS = 5
MIN_LEN = 200
MAX_LEN = 600
PAGE_RANGE = 256  

os.makedirs(DATASET_DIR, exist_ok=True)

def generate_dataset(idx):
    length = random.randint(MIN_LEN, MAX_LEN)
    pages = [random.randint(0, PAGE_RANGE - 1) for _ in range(length)]

    path = f"{DATASET_DIR}/dataset_{idx}.json"
    with open(path, "w") as f:
        json.dump(pages, f)

    print(f"[OK] Generated {path} ({length} references)")
    return path

if __name__ == "__main__":
    print("=== Generating Paging Datasets ===")
    for i in range(1, NUM_DATASETS + 1):
        generate_dataset(i)
    print("✅ Dataset generation complete.\n")
