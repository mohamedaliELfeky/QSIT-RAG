import logging
from utils.logging_utils.setup import setup_logging
# Setup logging
setup_logging(logging.INFO)

import os
from utils.configuration_files.configuration_reader import ConfigurationReader
from pipelines.indexing_pipeline import IndexingPipeline

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_indexing():
    # Ensure the data directory exists
    os.makedirs("./data/documents", exist_ok=True)
    
    # Path to your updated config.json
    config_path = "\\configuration\\application_config.json"
    
    try:
        # 1. Load Config
        logger.info(f"Loading configuration from {config_path}...")
        config = ConfigurationReader.load_config(config_path)
        
        # 2. Initialize Pipeline
        pipeline = IndexingPipeline(config)
        
        # 3. Run Pipeline
        logger.info("Starting the indexing process...")
        pipeline.run()
        
    except Exception as e:
        logger.error(f"An error occurred during pipeline execution: {e}")

if __name__ == "__main__":
    # Make sure to export OPENAI_API_KEY in your terminal before running
    run_indexing()