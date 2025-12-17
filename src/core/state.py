from typing import TypedDict, Optional, List, Dict, Any
from src.core.models import ProductData

class AgentState(TypedDict):
    # Inputs
    raw_text: str
    competitor_data: str
    
    # Internal Processing
    product_data: Optional[ProductData]
    generated_questions: List[Dict[str, str]] # This will become faq.json
    retry_count: int
    
    # Final Outputs (Publisher splits these)
    final_product_page: Dict[str, Any]      # product_page.json
    final_comparison_page: Dict[str, Any]   #  comparison_page.json