# src/content/tools.py
from langchain_core.tools import tool
from typing import List

@tool
def format_currency(amount: float, currency: str = "₹") -> str:
    """Formats a price amount into a standardized currency string."""
    return f"{currency}{int(amount)}"

@tool
def calculate_price_difference(price_a: float, price_b: float) -> str:
    """
    Calculates the difference between two prices and returns a text summary.
    Use this when comparing affordability.
    """
    diff = price_a - price_b
    if diff < 0:
        return f"Target product is ₹{abs(int(diff))} cheaper."
    elif diff > 0:
        return f"Target product is ₹{int(diff)} more expensive."
    return "Both products have the same price."

@tool
def analyze_ingredient_overlap(list_a: List[str], list_b: List[str]) -> str:
    """
    Compares two lists of ingredients to find common and unique elements.
    Returns a natural language summary.
    """
    set_a = set(x.lower() for x in list_a)
    set_b = set(x.lower() for x in list_b)
    
    common = set_a.intersection(set_b)
    unique_a = set_a - set_b
    
    response = []
    if common:
        response.append(f"Shared ingredients: {', '.join(common).title()}.")
    if unique_a:
        response.append(f"Unique advantages: {', '.join(unique_a).title()}.")
    
    return " ".join(response)

# Export tools list for the Agent to bind
PUBLISHER_TOOLS = [format_currency, calculate_price_difference, analyze_ingredient_overlap]