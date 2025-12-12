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
    
    # The structured data (populated by Analyst)
    product_data: Optional[ProductData]
    
    # The strategy outputs (populated by Strategist)
    generated_questions: Optional[List[Dict[str, str]]]
    
    # Context data (Mocked competitor)
    competitor_data: Optional[Dict[str, Any]]
    
    # Final Artifacts (populated by Publisher)
    final_faq_json: Optional[Dict]
    final_product_json: Optional[Dict]
    final_comparison_json: Optional[Dict]