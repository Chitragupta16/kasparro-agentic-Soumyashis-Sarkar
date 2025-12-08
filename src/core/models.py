# src/core/models.py
from typing import List, Optional
from pydantic import BaseModel, Field

# --- Internal Source of Truth ---
class ProductData(BaseModel):
    """
    The strict internal representation of the product.
    All agents will pass this object, not raw text.
    """
    name: str = Field(..., description="Commercial name of the product")
    price: float = Field(..., description="Price in base currency")
    # FIX: Removed 'default="₹"' to prevent Gemini SDK error
    currency: str = Field(description="Currency symbol") 
    ingredients: List[str] = Field(..., description="List of active ingredients")
    benefits: List[str] = Field(..., description="Key benefits provided")
    skin_type: List[str] = Field(..., description="Target skin types")
    usage_instructions: str = Field(..., description="Step-by-step usage guide")
    side_effects: str = Field(..., description="Known side effects or warnings")

# --- Output Schemas (JSON Artifacts) ---

# 1. FAQ Page Schema
class FAQItem(BaseModel):
    question: str
    answer: str
    category: str  # e.g., Safety, Usage, General

class FAQPage(BaseModel):
    page_title: str = "Frequently Asked Questions"
    product_name: str
    faqs: List[FAQItem]

# 2. Product Page Schema
class ProductPageSection(BaseModel):
    heading: str
    content: str

class ProductPage(BaseModel):
    title: str
    description: str
    price_display: str
    highlights: List[str]
    sections: List[ProductPageSection]

# 3. Comparison Page Schema
class ComparisonFeature(BaseModel):
    feature_name: str
    product_a_value: str
    product_b_value: str
    analysis: str  # Generated logic result (e.g., "A is cheaper")

class ComparisonPage(BaseModel):
    title: str
    product_a: str
    product_b: str
    comparison_table: List[ComparisonFeature]
    summary: str