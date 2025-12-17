from typing import List

def generate_safety_warning_block(ingredients: List[str]) -> str:
    """
    Generates a mandatory safety warning based on specific ingredients.
    This logic is deterministic: If 'X' is in ingredients, print 'Y'.
    """
    warnings = []
    
    # Normalize ingredients to lowercase for matching
    ing_lower = [i.lower() for i in ingredients]
    
    # Rule 1: Vitamin C / Acids
    if any(x in ing_lower for x in ["vitamin c", "ascorbic acid", "citric acid"]):
        warnings.append("Patch test recommended. May cause tingling sensation.")
        
    # Rule 2: Retinol
    if any(x in ing_lower for x in ["retinol", "retin-a"]):
        warnings.append("Use only at night. Wear sunscreen during the day.")
        
    # Default Warning
    if not warnings:
        return "Standard safety test recommended before full use."
        
    return " | ".join(warnings)