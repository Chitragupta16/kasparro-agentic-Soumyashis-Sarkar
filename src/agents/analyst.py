from langchain_google_genai import ChatGoogleGenerativeAI
from src.core.state import AgentState
from src.core.models import ProductData
import os
import time

class AnalystAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            temperature=0,
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

    def run(self, state: AgentState) -> dict:
        """
        Extracts structured product data from raw text AND competitor text.
        """
        print("--- [Analyst] Extracting Structured Data ---")
        # Safety sleep to handle rate limits
        time.sleep(2)

        # 1. Get both inputs
        raw_text = state.get("raw_text", "")
        competitor_text = state.get("competitor_data", "") 

        # Enforcing the Pydantic model 'ProductData' here
        structured_llm = self.llm.with_structured_output(ProductData)

        # 2. Update Prompt to handle both sources
        system_prompt = (
            "You are an expert Data Analyst. Extract data from the texts below. "
            "1. Extract the MAIN product details from the 'Main Product Text'. "
            "2. Extract the COMPETITOR price from the 'Competitor Text'. "
            "Ensure prices are numbers (e.g., 699, not '₹699')."
        )
        
        # 3. Combine inputs so the LLM sees the full context
        combined_input = f"""
        --- Main Product Text ---
        {raw_text}
        
        --- Competitor Text ---
        {competitor_text}
        """
        
        # Invoke the LLM
        result = structured_llm.invoke([
            ("system", system_prompt),
            ("user", combined_input)
        ])

        # Return the update for the state
        return {"product_data": result}