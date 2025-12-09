# src/agents/strategist.py
import json
from typing import List, Dict
from src.agents.base_agent import BaseAgent
from src.core.models import ProductData
from src.config import get_gemini_model

class StrategistAgent(BaseAgent):
    def __init__(self):
        super().__init__("Strategist")
        self.model = get_gemini_model()

    def process(self, product_data: ProductData) -> List[Dict[str, str]]:
        self.log(f"Brainstorming content for {product_data.name}...")

        prompt = f"""
        You are a Content Strategist.
        Based on the product data below, generate exactly 15 distinct user questions.
        
        Categorize them into: 'Safety', 'Usage', 'Benefits', 'General'.
        
        Product Context:
        Name: {product_data.name}
        Ingredients: {product_data.ingredients}
        Usage: {product_data.usage_instructions}
        Side Effects: {product_data.side_effects}

        Output strict JSON: A list of objects with keys: "question", "answer", "category".
        Make the answers helpful, professional, and based ONLY on the provided data.
        """

        result = self.model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )

        try:
            questions = json.loads(result.text)
            self.log(f"Generated {len(questions)} Q&A pairs.")
            return questions
        except Exception as e:
            self.log(f"Error parsing strategy output: {e}")
            raise e