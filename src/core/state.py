# src/core/state.py
from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict
from src.core.models import ProductData, FAQItem, ComparisonPage

class AgentState(TypedDict):
    """
    The shared memory of the Graph.
    Nodes (Agents) will modify this state as data flows through.
    """
    raw_text: str
    
    # The structured data (given by our analyst)
    product_data: Optional[ProductData]
    
    # The strategy outputs (given by our strategist)
    generated_questions: Optional[List[Dict[str, str]]]
    
    # Context data (the fictional competitor product)
    competitor_data: Optional[Dict[str, Any]]
    
    # Final Artifacts (given by our publisher)
    final_faq_json: Optional[Dict]
    final_product_json: Optional[Dict]
    final_comparison_json: Optional[Dict]