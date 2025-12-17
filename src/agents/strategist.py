from langchain_google_genai import ChatGoogleGenerativeAI
from src.core.state import AgentState
from src.core.models import FAQPage
import os

class StrategistAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            temperature=0.8,
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

    def run(self, state: AgentState) -> dict:
        print("--- [Strategist] Brainstorming Questions ---")
        product_data = state.get("product_data")
        
        # Get current retry count, default to 0
        current_retries = state.get("retry_count", 0)
        
        structured_llm = self.llm.with_structured_output(FAQPage)

        # If this is a retry, we can inject a stronger prompt
        if current_retries > 0:
            print(f"   >>> Retry #{current_retries}: Demanding more questions...")
            instruction = "PREVIOUS ATTEMPT FAILED. You MUST generate at least 5 distinct questions."
        else:
            instruction = "Brainstorm 5 distinct, high-value questions."

        system_prompt = (
            f"You are a Content Strategist. Analyze this product: {product_data.name}. "
            f"{instruction} "
            "Focus on: Price, Safety, Ingredients, and Usage. "
            "Return a list of objects with 'question' and 'category'."
        )

        result = structured_llm.invoke(system_prompt)
        
        questions_list = [q.dict() for q in result.faqs]
        
        return {
    "generated_questions": questions_list,
    "retry_count": current_retries + 1  # <--- CRITICAL UPDATE
}