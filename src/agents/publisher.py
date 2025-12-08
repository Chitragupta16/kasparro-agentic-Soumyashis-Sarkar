# src/agents/publisher.py
import json
import os
from src.agents.base_agent import BaseAgent
from src.content.templates import TemplateEngine
from src.core.models import ProductData

class PublisherAgent(BaseAgent):
    def __init__(self):
        super().__init__("Publisher")
        self.output_dir = "data/output"

    def process(self, payload: dict):
        """
        Payload expects:
        {
            "product_data": ProductData object,
            "questions": List[dict],
            "competitor_data": dict
        }
        """
        self.log("Starting final page assembly...")
        
        p_data = payload["product_data"]
        questions = payload["questions"]
        comp_data = payload["competitor_data"]

        # 1. Generate FAQ Page
        self.log("Rendering FAQ Page...")
        faq_page = TemplateEngine.render_faq_template(p_data, questions)
        self._save_json("faq.json", faq_page)

        # 2. Generate Product Page
        self.log("Rendering Product Page...")
        prod_page = TemplateEngine.render_product_page_template(p_data)
        self._save_json("product_page.json", prod_page)

        # 3. Generate Comparison Page
        self.log("Rendering Comparison Page...")
        comp_page = TemplateEngine.render_comparison_template(p_data, comp_data)
        self._save_json("comparison_page.json", comp_page)
        
        self.log("All pages published to data/output/.")

    def _save_json(self, filename: str, data: dict):
        path = os.path.join(self.output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)