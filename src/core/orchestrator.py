# src/core/orchestrator.py
import logging
from src.agents.analyst import AnalystAgent
from src.agents.strategist import StrategistAgent
from src.agents.publisher import PublisherAgent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class Orchestrator:
    def __init__(self):
        self.logger = logging.getLogger("Orchestrator")
        # Initialize Agents
        self.analyst = AnalystAgent()
        self.strategist = StrategistAgent()
        self.publisher = PublisherAgent()

        # Define Fictional Competitor Data (Hardcoded as per assignment requirement)
        self.competitor_data = {
            "name": "DermaGlow Generic Serum",
            "price": 450.0,
            "ingredients": ["Vitamin C", "Water", "Glycerin"],
            "benefits": ["Basic hydration", "Mild brightening"]
        }

    def run_pipeline(self, raw_input_text: str):
        """
        Executes the linear automation graph (DAG).
        Flow: Raw Text -> [Analyst] -> Structured Data -> [Strategist] -> Q&A -> [Publisher] -> JSON Files
        """
        self.logger.info("Starting Agentic Pipeline...")

        # Step 1: Ingestion (Analyst Agent)
        # Dependency: Raw Text
        self.logger.info("--- Step 1: Analyst Agent (Ingestion) ---")
        product_model = self.analyst.process(raw_input_text)
        
        # Step 2: Ideation (Strategist Agent)
        # Dependency: Product Model
        self.logger.info("--- Step 2: Strategist Agent (Ideation) ---")
        generated_questions = self.strategist.process(product_model)

        # Step 3: Assembly (Publisher Agent)
        # Dependency: Product Model + Questions + Competitor Data
        self.logger.info("--- Step 3: Publisher Agent (Assembly) ---")
        payload = {
            "product_data": product_model,
            "questions": generated_questions,
            "competitor_data": self.competitor_data
        }
        self.publisher.process(payload)

        self.logger.info("Pipeline completed successfully. Check 'data/output/'.")