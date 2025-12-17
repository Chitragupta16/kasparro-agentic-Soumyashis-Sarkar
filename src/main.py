import os
import sys
import json
from dotenv import load_dotenv

# 1. Load env variables
load_dotenv()

if not os.getenv("GEMINI_API_KEY"):
    print("[ERROR] GEMINI_API_KEY not found. Please check your .env file.")
    sys.exit(1)

from src.core.graph import build_graph

def main():
    raw_text = """
    Product: SuperBoost Vitamin C Serum
    Price: ₹699
    Ingredients: Vitamin C, Hyaluronic Acid, Ferulic Acid, Vitamin E.
    Description: A powerful serum that brightens skin and reduces dark spots. 
    Use daily for best results. No parabens.
    """
    
    competitor_data = """
    Product: GlowX Serum
    Price: ₹450
    """

    print("Initializing LangGraph Pipeline...")
    app = build_graph()
    
    # Run the graph
    result = app.invoke({
        "raw_text": raw_text,
        "competitor_data": competitor_data
    })
    
    print("\n--- Pipeline Finished ---")
    os.makedirs("data/output", exist_ok=True)

    # 1. Save FAQ.json (From Strategist)
    if result.get("generated_questions"):
        with open("data/output/faq.json", "w") as f:
            json.dump({"faqs": result["generated_questions"]}, f, indent=2)
            print("Saved: data/output/faq.json")

    # 2. Save Product_Page.json (From Publisher)
    if result.get("final_product_page"):
        with open("data/output/product_page.json", "w") as f:
            json.dump(result["final_product_page"], f, indent=2)
            print("Saved: data/output/product_page.json")

    # 3. Save Comparison_Page.json (From Publisher)
    if result.get("final_comparison_page"):
        with open("data/output/comparison_page.json", "w") as f:
            json.dump(result["final_comparison_page"], f, indent=2)
            print("Saved: data/output/comparison_page.json")

if __name__ == "__main__":
    main()