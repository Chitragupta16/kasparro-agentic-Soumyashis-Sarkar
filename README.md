# Kasparro Agentic Content System

This is my submission for the Kasparro Applied AI Engineer challenge. It is a modular agentic system built with **LangChain** and **LangGraph** that autonomously converts raw product data into structured content pages (FAQ, Product Page, Comparison).

## Note
I put the detailed system design and architectural diagram in `docs/projectdocumentation.md`.

## How It Works

I avoided the "monolith script" approach. Instead, I implemented a **StateGraph** (DAG) where data flows between three specialized nodes:

1.  **Analyst Node (Ingestion):** It parses raw text using a LangChain `PydanticOutputParser`. This enforces a strict `ProductData` schema immediately. If the input is bad, the pipeline fails early rather than pushing forward errors in the pipeline.
2.  **Strategist Node (Ideation):** It receives the structured context and generates 15+ user-centric questions.
3.  **Publisher Node (Assembly & Tools):** It unctions as the acting layer. Unlike a standard template engine, this agent has access to custom **Tools** (Python functions). It invokes these tools to perform accurate calculations (like price comparisons) before assembling the final JSON output.

## Setup

I used Python 3.10+ and the Google Gemini API (specifically `gemini-1.5-flash`).

1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/Chitragupta16/kasparro-agentic-Soumyashis-Sarkar.git](https://github.com/Chitragupta16/kasparro-agentic-Soumyashis-Sarkar.git)
    cd kasparro-agentic-Soumyashis-Sarkar
    ```

2.  **Install requirements:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file in the root folder:
    ```env
    GEMINI_API_KEY=your_actual_key_here
    ```

## Running the Pipeline

To execute the graph (Analyst -> Strategist -> Publisher), run:

```bash
python -m src.main

```
## Output

Artifacts are generated in the data/output/ folder:

1. **faq.json**

2. **product_page.json**

3. **comparison_page.json**

## Logic & Design
I used LangGraph to maintain a shared state object passed between nodes, rather than passing loose variables around.

For logic like price differences, I bound Python functions as Tools to the Publisher agent. This prevents the LLM from attempting (and often failing at) maths.

## Note
I used Copilot to assist with code commenting and documentation generation.