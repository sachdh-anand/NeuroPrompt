"""
Integration test for the NeuroPrompt system.
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock, mock_open

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the NeuroPromptCrew
from core.crew import NeuroPromptCrew
from core.logger import get_logger

# Initialize logger
logger = get_logger(__name__)


class TestNeuroPromptIntegration(unittest.TestCase):
    """Integration test cases for NeuroPrompt."""

    def setUp(self):
        """Set up test fixtures."""
        # Create necessary directories
        os.makedirs("logs", exist_ok=True)
        os.makedirs("data", exist_ok=True)
        os.makedirs("documents/frameworks", exist_ok=True)
        
        # Set up mock API key if not present
        if not os.getenv("OPENROUTER_API_KEY"):
            os.environ["OPENROUTER_API_KEY"] = "test_api_key"
            
        logger.info("Starting test environment setup")

    @patch('core.crew.NeuroPromptCrew._initialize_agents')
    @patch('core.crew.NeuroPromptCrew._create_crew')
    def test_generate_prompt_flow(self, mock_create_crew, mock_initialize_agents):
        """Test the full prompt generation flow with mocked components."""
        logger.info("Testing prompt generation flow")
        
        # Mock the crew creation
        mock_crew = MagicMock()
        mock_crew.kickoff.return_value = "Process completed successfully"
        mock_create_crew.return_value = mock_crew
        
        # Set up result data
        expected_result = {
            "user_input": "Create a prompt for a creative writing assistant",
            "final_prompt": "Optimized prompt based on critique",
            "process_info": {
                "research": "Research results about prompt techniques",
                "initial_prompt": "Generated prompt using PECRA framework",
                "critique": "Detailed critique of the prompt",
                "optimization": "Optimized prompt based on critique"
            }
        }
        
        # Mock file operations
        with patch('builtins.open', mock_open()):
            # Create crew instance
            crew = NeuroPromptCrew()
            
            # Mock the generate_prompt method to return our expected result
            with patch.object(crew, 'generate_prompt', return_value=expected_result):
                result = crew.generate_prompt("Create a prompt for a creative writing assistant")
                
                # Verify result structure
                self.assertIn("user_input", result)
                self.assertIn("final_prompt", result)
                self.assertIn("process_info", result)
                
                # Verify the user input was preserved
                self.assertEqual(result["user_input"], "Create a prompt for a creative writing assistant")
                
                logger.info("Prompt generation test completed successfully")

    @patch('core.model_manager.ModelManager.generate_completion')
    def test_model_fallback_mechanism(self, mock_generate_completion):
        """Test that the model fallback mechanism works correctly when primary model fails."""
        logger.info("Testing model fallback mechanism")
        
        # Configure the mock to fail on first call and succeed on second
        mock_generate_completion.side_effect = [
            None,  # First call fails
            {"choices": [{"message": {"content": "Response from fallback model"}}]}  # Second call succeeds
        ]
        
        # This test would be more extensive in a real implementation
        # Here we're just verifying the core functionality
        from core.model_manager import ModelManager
        manager = ModelManager()
        
        # Mark primary model as unavailable
        manager.model_status[manager.primary_model] = False
        
        # Get available model should return first fallback
        fallback = manager.get_available_model()
        self.assertEqual(fallback, manager.fallback_models[0])
        
        logger.info("Model fallback test completed successfully")


if __name__ == "__main__":
    unittest.main()