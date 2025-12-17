import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from src.core.state import AgentState
import time
from src.content.tools import calculate_price_difference, format_currency
from src.content.blocks import generate_safety_warning_block

class PublisherAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            temperature=0.2,
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

    def run(self, state: AgentState) -> dict:
        print("--- [Publisher] Assembling Product & Comparison Artifacts ---")
        time.sleep(2) #---for handling API rate limits
        
        # 1. Retrieve Data
        product = state.get("product_data")
        competitor_price = product.competitor_price 
        if competitor_price == 0.0:
            competitor_price = 450
            print("[Warning] Competitor price extraction failed. Using default.")
        
        # 2. Run Tools
        price_analysis = calculate_price_difference(price_a=product.price, price_b=competitor_price)
        safety_block = generate_safety_warning_block(product.ingredients)
        
        # 3. Construct Prompt for DUAL OUTPUT
        system_prompt = f"""
        You are a Content Publisher. Create two distinct JSON artifacts for the frontend.

        --- INPUT DATA ---
        Product: {product.name} ({format_currency(product.price)})
        Ingredients: {', '.join(product.ingredients)}
        Math Rule: {price_analysis}
        Safety Rule: {safety_block}

        --- OUTPUT REQUIREMENTS ---
        Return a SINGLE JSON object with exactly these two keys:

        1. "product_content": {{
            "title": "Marketing Title",
            "description": "Polished description",
            "safety_notice": "{safety_block}", 
            "specs": {{ ... }}
        }}

        2. "comparison_content": {{
            "summary": "Why we win",
            "price_verdict": "{price_analysis}",
            "competitor_price": "{format_currency(competitor_price)}"
        }}
        """

        response = self.llm.invoke(system_prompt)
        
        # 4. Parse & Split
        try:
            # Handle list/string issues from Gemini
            raw_content = response.content
            if isinstance(raw_content, list):
                text_content = "".join([str(item) for item in raw_content])
            else:
                text_content = str(raw_content)

            clean_text = text_content.replace("```json", "").replace("```", "").strip()
            full_data = json.loads(clean_text)
            
            return {
                "final_product_page": full_data.get("product_content", {}),
                "final_comparison_page": full_data.get("comparison_content", {})
            }
            
        except Exception as e:
            print(f"[Error] Publisher failed: {e}")
            return {
                "final_product_page": {}, 
                "final_comparison_page": {}
            }