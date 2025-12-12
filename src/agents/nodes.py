# src/agents/nodes.py
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.core.state import AgentState
from src.core.models import ProductData, FAQPage, ComparisonPage, ProductPage
from src.content.tools import PUBLISHER_TOOLS
from src.config import API_KEY

# Initializing the LLM here
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest", 
    google_api_key=API_KEY, 
    temperature=0
)

# Node 1: Analyst (Ingestion)
def analyst_node(state: AgentState):
    print("--- [Analyst] Extracting Structured Data ---")
    
    structured_llm = llm.with_structured_output(ProductData)
    prompt = ChatPromptTemplate.from_template(
        "Extract the following product text into a strict data object: {text}"
    )
    chain = prompt | structured_llm
    result = chain.invoke({"text": state["raw_text"]})
    
    return {"product_data": result}

# Node 2: Strategist (Ideation)
def strategist_node(state: AgentState):
    print("--- [Strategist] Brainstorming Questions ---")
    
    # We want a list of FAQs, so we define a wrapper schema for the whole
    # (Using the FAQPage schema from models.py as the target structure here)
    structured_llm = llm.with_structured_output(FAQPage)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a content strategist. Generate 15 distinct user questions based on the product data."),
        ("human", "Product Name: {name}\nDetails: {details}\n\nGenerate a FAQ Page structure.")
    ])
    
    # Serialize product data for prompt
    p_data = state["product_data"]
    details = f"Ingredients: {p_data.ingredients}, Usage: {p_data.usage_instructions}, Benefits: {p_data.benefits}"
    
    chain = prompt | structured_llm
    result = chain.invoke({"name": p_data.name, "details": details})
    return {"generated_questions": [item.dict() for item in result.faqs]}

# Node 3: Publisher (Assembly with Tools)
def publisher_node(state: AgentState):
    print("--- [Publisher] Assembling Final Pages ---")
    
    p_data = state["product_data"]
    comp_data = state["competitor_data"]
    
    # A. Create Product Page JSON
    # We ask the LLM to format it, potentially using tools if needed (though mostly formatting here)
    prod_llm = llm.with_structured_output(ProductPage)
    prod_prompt = ChatPromptTemplate.from_template(
        "Create a marketing product page for {name}. Price: {price}. Benefits: {benefits}. Use professional tone."
    )
    prod_page = (prod_prompt | prod_llm).invoke({
        "name": p_data.name, 
        "price": p_data.price, 
        "benefits": ", ".join(p_data.benefits)
    })
    
    # B. Create Comparison Page
    comp_llm = llm.bind_tools(PUBLISHER_TOOLS).with_structured_output(ComparisonPage)
    
    comp_prompt = ChatPromptTemplate.from_messages([
        ("system", "Compare these two products. Use the 'calculate_price_difference' and 'analyze_ingredient_overlap' tools to derive insights."),
        ("human", "Product A: {a_name} (${a_price}), Ing: {a_ing}\nProduct B: {b_name} (${b_price}), Ing: {b_ing}")
    ])
    
    comp_page = (comp_prompt | comp_llm).invoke({
        "a_name": p_data.name, "a_price": p_data.price, "a_ing": p_data.ingredients,
        "b_name": comp_data["name"], "b_price": comp_data["price"], "b_ing": comp_data["ingredients"]
    })

    return {
        "final_product_json": prod_page.dict(),
        "final_comparison_json": comp_page.dict(),
        "final_faq_json": {"faqs": state["generated_questions"]} # Pass through
    }