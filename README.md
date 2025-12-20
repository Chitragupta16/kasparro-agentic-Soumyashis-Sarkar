# Kasparro Agentic Content System

This is my submission for the Kasparro Applied AI Engineer challenge. It is a modular agentic system built with **LangChain** and **LangGraph** that autonomously converts raw product data into structured content pages (FAQ, Product Page, Comparison).

## Note
I put the detailed system design and architectural diagram in `docs/projectdocumentation.md`.

## How It Works

I avoided the "monolith script" approach. Instead, I implemented a **StateGraph** (DAG) where data flows between three specialized nodes with intelligent feedback loops:

1.  **Analyst Node (Ingestion):** It parses raw text using structured output parsers to enforce a strict `ProductData` schema immediately. Crucially, it now **dynamically extracts competitor pricing** from unstructured text, allowing for real-time market comparison without hardcoded values.
2.  **Strategist Node (Ideation):** It receives the structured context and generates 15+ user-centric questions. I implemented a **Self-Correction Loop** here: if the agent generates fewer than 15 questions, the graph automatically rejects the output and forces a retry with a stronger prompt.
3.  **Publisher Node (Assembly & Tools):** It functions as the acting layer. Unlike a standard template engine, this agent uses **Deterministic Tools** (pure Python functions) to calculate price differences accurately before assembling the final JSON artifacts.

## Setup

I used Python 3.10+ and the Google Gemini API (specifically `gemini-flash-latest`).

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

1. Self-Correction: I utilized Conditional Edges to implement a "Retry" mechanism. This ensures the Strategist meets quality standards (15+ FAQs) before passing control downstream.

2. Deterministic Math: For logic like price differences, I created Python functions that the Publisher agent can call. I removed the Tools to fix the broken tools issue. This prevents the LLM from attempting (and often failing at) arithmetic.

## Note
I used Copilot to assist with code commenting and documentation generation.
