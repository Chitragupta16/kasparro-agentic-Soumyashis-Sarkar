# Kasparro Agentic Content System- My submission

This is my submission for the Kasparro Applied AI Engineer challenge. It’s a modular system that takes raw product data and uses a team of agents to generate structured content pages (FAQ, Product Page, Comparison) automatically.

I focused on building a clean pipeline where logic is deterministic, ie, the code and creativity is handled by the LLM,ie the agents.

## How It Works

I avoided the "monolith script" approach, as was mentioned. Instead, I built a DAG with three distinct agents:

1.  **Analyst Agent (Ingestion):** It takes the raw text and forces it into a strict Pydantic model (`ProductData`). If the data doesn't fit the schema, it should break early rather than hallucinating.
2.  **Strategist Agent (Ideation):** Takes that structured data and brainstorms 15+ user questions tagged by category.
3.  **Publisher Agent (Assembly):** This one doesn't use an LLM. It uses a custom Template Engine and Python logic blocks to assemble the final JSON files. This ensures math (like price comparisons) is always accurate.

## Setup

I used Python 3.10+ and a Google Gemini API key ( which is free (gemini-flash-latest)).

1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/Chitragupta16/kasparro-agentic-Soumyashis-Sarkar.git](https://github.com/Chitragupta16/kasparro-agentic-Soumyashis-Sarkar)
    cd kasparro-agentic-Soumyashis-Sarkar
    ```

2.  **Install requirements:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Add your key:**
    Create a `.env` file in the root folder:
    ```env
    GEMINI_API_KEY=your_actual_key_here
    ```

## Running the Pipeline

To run the full flow (Analyst -> Strategist -> Publisher), run this command from the root directory:

```bash
python -m src.main
```
## Output

Check the `data/output/` folder. You'll see three files generated:
* `faq.json`
* `product_page.json`
* `comparison_page.json`

## Logic & Design

I used **Pydantic** for everything to ensure the agents talk to each other using strict objects, not loose strings. For the comparison logic (like calculating price differences), I wrote standard Python functions instead of asking the AI to do math, which keeps it reliable. 


# Note
I took the help of Copilot for documentation in the comments of the code