# src/main.py
import os
import sys
from src.core.orchestrator import Orchestrator

def load_input_data(filepath: str) -> str:
    if not os.path.exists(filepath):
        print(f"Error: Input file '{filepath}' not found.")
        sys.exit(1)
    
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def main():
    # Define paths
    input_path = os.path.join("data", "input", "product_data.txt")
    
    # 1. Load Data
    print(f"Loading data from {input_path}...")
    raw_text = load_input_data(input_path)
    
    # 2. Initialize Orchestrator
    orchestrator = Orchestrator()
    
    # 3. Run
    try:
        orchestrator.run_pipeline(raw_text)
    except Exception as e:
        print(f"Pipeline Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()