#!/usr/bin/env python3
"""
Quick test script for NeuroPrompt functionality.
"""
import os
import sys
import logging
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Ensure necessary directories exist
os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/test.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("test")

# Load environment variables
load_dotenv()

def test_model_manager():
    """Test the ModelManager functionality."""
    from core.model_manager import ModelManager
    
    logger.info("Testing ModelManager...")
    
    # Check if API key is available
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logger.warning("OPENROUTER_API_KEY not found in environment. Using dummy key for tests.")
        os.environ["OPENROUTER_API_KEY"] = "dummy_key_for_testing"
    
    # Create ModelManager
    try:
        manager = ModelManager()
        logger.info(f"ModelManager initialized successfully")
        logger.info(f"Primary model: {manager.primary_model}")
        logger.info(f"Fallback models: {manager.fallback_models}")
        logger.info(f"Model status: {manager.get_models_status()}")
        return True
    except Exception as e:
        logger.error(f"Error initializing ModelManager: {str(e)}")
        return False

def test_agents():
    """Test agent initialization."""
    logger.info("Testing agent initialization...")
    
    # Check if API key is available
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logger.warning("OPENROUTER_API_KEY not found in environment. Using dummy key for tests.")
        os.environ["OPENROUTER_API_KEY"] = "dummy_key_for_testing"
    
    try:
        # Test PromptGeneratorAgent
        from agents.prompt_generator import PromptGeneratorAgent
        generator = PromptGeneratorAgent(model="test-model")
        generator_agent = generator.get_agent()
        logger.info(f"PromptGeneratorAgent initialized successfully")
        
        # Test ResearcherAgent
        from agents.researcher import ResearcherAgent
        researcher = ResearcherAgent(model="test-model")
        researcher_agent = researcher.get_agent()
        logger.info(f"ResearcherAgent initialized successfully")
        
        # Test CriticAgent
        from agents.critic import CriticAgent
        critic = CriticAgent(model="test-model")
        critic_agent = critic.get_agent()
        logger.info(f"CriticAgent initialized successfully")
        
        # Test OptimizerAgent
        from agents.optimizer import OptimizerAgent
        optimizer = OptimizerAgent(model="test-model")
        optimizer_agent = optimizer.get_agent()
        logger.info(f"OptimizerAgent initialized successfully")
        
        return True
    except Exception as e:
        logger.error(f"Error initializing agents: {str(e)}")
        return False

def test_crew():
    """Test crew initialization."""
    logger.info("Testing crew initialization...")
    
    # Check if API key is available
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logger.warning("OPENROUTER_API_KEY not found in environment. Using dummy key for tests.")
        os.environ["OPENROUTER_API_KEY"] = "dummy_key_for_testing"
    
    try:
        from core.crew import NeuroPromptCrew
        crew = NeuroPromptCrew()
        logger.info(f"NeuroPromptCrew initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Error initializing NeuroPromptCrew: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("Running NeuroPrompt quick tests...")
    
    # Run tests
    model_manager_result = test_model_manager()
    agents_result = test_agents()
    crew_result = test_crew()
    
    # Print results
    print("\nTest Results:")
    print(f"ModelManager: {'✅ PASS' if model_manager_result else '❌ FAIL'}")
    print(f"Agents: {'✅ PASS' if agents_result else '❌ FAIL'}")
    print(f"Crew: {'✅ PASS' if crew_result else '❌ FAIL'}")
    
    # Overall result
    if model_manager_result and agents_result and crew_result:
        print("\n✅ All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())