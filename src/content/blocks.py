# src/content/blocks.py
from typing import List, Dict, Any

def format_currency_block(amount: float, currency: str = "₹") -> str:
    """
    Transforms raw float price into formatted string.
    Rule: Always integer amounts for this brand tone.
    """
    return f"{currency}{int(amount)}"

def compare_ingredients_block(list_a: List[str], list_b: List[str]) -> str:
    """
    Logic: Identifies common vs unique ingredients.
    Returns a textual analysis string.
    """
    set_a = set(x.lower() for x in list_a)
    set_b = set(x.lower() for x in list_b)
    
    common = set_a.intersection(set_b)
    unique_a = set_a - set_b
    
    response = []
    if common:
        response.append(f"Both products rely on {', '.join(common).title()}.")
    if unique_a:
        response.append(f"GlowBoost adds {', '.join(unique_a).title()} for extra efficacy.")
    
    return " ".join(response)

def compare_price_block(price_a: float, price_b: float, currency: str = "₹") -> str:
    """
    Logic: Calculates absolute difference and declares relative affordability.
    """
    diff = price_a - price_b
    if diff < 0:
        return f"GlowBoost is {currency}{abs(int(diff))} more affordable."
    elif diff > 0:
        return f"Product B is {currency}{int(diff)} cheaper."
    return "Both products are priced identically."

def generate_safety_warning_block(side_effects: str) -> str:
    """
    Logic: If side effects exist, wrap in a standard disclaimer.
    """
    if not side_effects or side_effects.lower() == "none":
        return "Safe for daily use."
    return f"⚠️ Advisory: {side_effects}. Perform a patch test before full application."

# Registry for the Template Engine to access functions by name
BLOCK_REGISTRY = {
    "format_currency": format_currency_block,
    "compare_ingredients": compare_ingredients_block,
    "compare_price": compare_price_block,
    "generate_safety_warning": generate_safety_warning_block
}