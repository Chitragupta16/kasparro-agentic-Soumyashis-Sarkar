# src/main.py
import os
import json
from src.core.graph import build_graph

def main():
    # 1. Load Input
    input_path = os.path.join("data", "input", "product_data.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
        
    # 2. Define the competitor(Context)
    competitor_data = {
        "name": "DermaGlow Generic Serum",
        "price": 450.0,
        "ingredients": ["Vitamin C", "Water", "Glycerin"],
    }
    
    # 3. Run Graph
    print("Initializing LangGraph Pipeline...")
    app = build_graph()
    
    result = app.invoke({
        "raw_text": raw_text,
        "competitor_data": competitor_data
    })
    
    # 4. Save Outputs to the data/output
    output_dir = os.path.join("data", "output")
    os.makedirs(output_dir, exist_ok=True)
    
    print("Saving artifacts...")
    with open(os.path.join(output_dir, "product_page.json"), "w") as f:
        json.dump(result["final_product_json"], f, indent=2)
        
    with open(os.path.join(output_dir, "comparison_page.json"), "w") as f:
        json.dump(result["final_comparison_json"], f, indent=2)
        
    with open(os.path.join(output_dir, "faq.json"), "w") as f:
        json.dump(result["final_faq_json"], f, indent=2)
        
    print("Pipeline Finished Successfully.")

if __name__ == "__main__":
    main()