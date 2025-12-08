# src/content/templates.py
from typing import Dict, Any, List
from src.content.blocks import BLOCK_REGISTRY
from src.core.models import ProductData

class TemplateEngine:
    """
    Orchestrates the assembly of pages by combining:
    1. Static Structures (Templates)
    2. Dynamic Data (ProductData)
    3. Logical Rules (Blocks)
    """

    @staticmethod
    def render_faq_template(data: ProductData, questions: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Assembles the FAQ page structure.
        Note: Questions are injected from the Strategist Agent.
        """
        return {
            "page_title": f"Common Questions about {data.name}",
            "product_name": data.name,
            "faqs": [
                {
                    "question": q["question"],
                    "answer": q["answer"],
                    "category": q["category"]
                }
                for q in questions
            ]
        }

    @staticmethod
    def render_product_page_template(data: ProductData) -> Dict[str, Any]:
        """
        Assembles the Product Page using Logic Blocks for formatted fields.
        """
        # invoke logic blocks
        fmt_price = BLOCK_REGISTRY["format_currency"](data.price, data.currency)
        safety_msg = BLOCK_REGISTRY["generate_safety_warning"](data.side_effects)
        
        return {
            "title": data.name,
            "description": f"Experience the power of {', '.join(data.ingredients)}.",
            "price_display": fmt_price,
            "highlights": data.benefits,
            "sections": [
                {
                    "heading": "How to Use",
                    "content": data.usage_instructions
                },
                {
                    "heading": "Safety Information",
                    "content": safety_msg
                }
            ]
        }

    @staticmethod
    def render_comparison_template(data_a: ProductData, data_b: dict) -> Dict[str, Any]:
        """
        Assembles a comparison against a competitor.
        This demonstrates the use of comparative logic blocks.
        """
        # Logic Block Executions
        price_analysis = BLOCK_REGISTRY["compare_price"](data_a.price, data_b["price"])
        ing_analysis = BLOCK_REGISTRY["compare_ingredients"](data_a.ingredients, data_b["ingredients"])

        return {
            "title": f"{data_a.name} vs {data_b['name']}",
            "product_a": data_a.name,
            "product_b": data_b["name"],
            "summary": f"While both products target similar concerns, {price_analysis}",
            "comparison_table": [
                {
                    "feature_name": "Price Point",
                    "product_a_value": str(data_a.price),
                    "product_b_value": str(data_b["price"]),
                    "analysis": price_analysis
                },
                {
                    "feature_name": "Key Ingredients",
                    "product_a_value": ", ".join(data_a.ingredients),
                    "product_b_value": ", ".join(data_b["ingredients"]),
                    "analysis": ing_analysis
                }
            ]
        }