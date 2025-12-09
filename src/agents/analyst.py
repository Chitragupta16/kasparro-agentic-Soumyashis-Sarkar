# src/agents/analyst.py
import json
import typing_extensions as typing
from src.agents.base_agent import BaseAgent
from src.core.models import ProductData
from src.config import get_gemini_model

class AnalystAgent(BaseAgent):
    def __init__(self):
        super().__init__("Analyst")
        self.model = get_gemini_model()

    def process(self, raw_text: str) -> ProductData:
        self.log("Analyzing raw input data...")

        prompt = f"""
        You are an expert Data Analyst. 
        Analyze the following product text and extract it into a strict JSON format.
        
        Raw Text:
        {raw_text}
        
        Ensure lists like ingredients and benefits are clean strings.Price should be a float.
        """

        # Force Gemini to output strictly adhering to the Pydantic model
        result = self.model.generate_content(
            prompt,
            generation_config=dict(
                response_mime_type="application/json",
                response_schema=ProductData
            )
        )
        

        try:
            data_dict = json.loads(result.text)
            product_data = ProductData(**data_dict)
            self.log("Data successfully structured.")
            return product_data
        except Exception as e:
            self.log(f"Error parsing model output: {e}")
            raise e