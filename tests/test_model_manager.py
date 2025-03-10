"""
Test script for the ModelManager class.
"""
import os
import sys
import unittest
import requests
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

# Add parent directory to path to import from core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the ModelManager and logger
from core.model_manager import ModelManager
from core.logger import get_logger, LogSymbols

# Initialize logger
logger = get_logger(__name__)

# Load environment variables
load_dotenv()


class TestModelManager(unittest.TestCase):
    """Test cases for the ModelManager class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create directories if they don't exist
        os.makedirs("logs", exist_ok=True)
        
        # Mock environment variables if not present
        if not os.getenv("OPENROUTER_API_KEY"):
            os.environ["OPENROUTER_API_KEY"] = "test_api_key"
            logger.warning("Using mock API key - API responses will be simulated")
        
        logger.info("Starting test environment setup")
        
    def tearDown(self):
        """Clean up after tests."""
        logger.info("Test completed successfully")
        
    def test_initialization(self):
        """Test if ModelManager initializes correctly."""
        logger.info("Starting ModelManager initialization test")
        manager = ModelManager()
        self.assertIsNotNone(manager.api_key)
        self.assertIsNotNone(manager.primary_model)
        self.assertTrue(len(manager.fallback_models) > 0)
        self.assertTrue(all(model in manager.model_status for model in manager.fallback_models))
        logger.info("ModelManager initialization completed with %d fallback models", 
                   len(manager.fallback_models))
        
    def test_get_available_model(self):
        """Test if get_available_model returns the correct model."""
        logger.info("Starting model availability test")
        manager = ModelManager()
        
        # Initially, primary model should be available
        self.assertEqual(manager.get_available_model(), manager.primary_model)
        logger.info("Primary model verified as available")
        
        # Mark primary as unavailable
        manager.model_status[manager.primary_model] = False
        logger.warning("Primary model marked as unavailable")
        
        # Should return first fallback
        fallback = manager.get_available_model()
        self.assertEqual(fallback, manager.fallback_models[0])
        logger.info("Fallback mechanism activated - using '%s'", fallback)
        
        # Mark all models as unavailable
        for model in manager.model_status:
            manager.model_status[model] = False
        logger.warning("Testing recovery - all models unavailable")
        
        # Should reset and return primary
        recovered_model = manager.get_available_model()
        self.assertEqual(recovered_model, manager.primary_model)
        logger.info("Recovery successful - restored to primary model")
        
    @patch('requests.post')
    def test_generate_completion(self, mock_post):
        """Test generate_completion with mocked API response."""
        logger.info("Starting completion generation test")
        
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {"choices": [{"message": {"content": "Test response"}}]}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        manager = ModelManager()
        messages = [{"role": "user", "content": "Hello"}]
        
        logger.info("Sending test request to API")
        response = manager.generate_completion(messages)
        
        self.assertIsNotNone(response)
        self.assertIn("choices", response)
        self.assertEqual(response["choices"][0]["message"]["content"], "Test response")
        logger.info("API response received successfully")
        
    @patch('requests.post')
    def test_fallback_mechanism(self, mock_post):
        """Test fallback mechanism when primary model fails."""
        logger.info("Starting fallback mechanism test")
        
        # First call raises exception, second succeeds
        mock_post.side_effect = [
            requests.exceptions.RequestException("Model unavailable"),
            MagicMock(**{
                "json.return_value": {"choices": [{"message": {"content": "Fallback response"}}]},
                "raise_for_status.return_value": None
            })
        ]
        
        manager = ModelManager()
        messages = [{"role": "user", "content": "Hello"}]
        
        logger.warning("Simulating primary model failure")
        response = manager.generate_completion(messages)
        
        self.assertIsNotNone(response)
        self.assertIn("choices", response)
        self.assertEqual(response["choices"][0]["message"]["content"], "Fallback response")
        logger.info("Fallback handled successfully")
        
    def test_reset_model_status(self):
        """Test resetting model status."""
        logger.info("Starting model status reset test")
        manager = ModelManager()
        
        # Mark all models as unavailable
        for model in manager.model_status:
            manager.model_status[model] = False
        logger.warning("All models marked as unavailable")
            
        # Reset status
        logger.info("Initiating status reset")
        manager.reset_model_status()
        
        # Verify all models are available
        self.assertTrue(all(manager.model_status.values()))
        logger.info("All models restored to available state")
        
    @patch('requests.post')
    def test_all_models_fail(self, mock_post):
        """Test behavior when all models fail."""
        logger.info("Starting catastrophic failure test")
        
        # Make all API calls fail
        mock_post.side_effect = requests.exceptions.RequestException("All models unavailable")
        
        manager = ModelManager()
        messages = [{"role": "user", "content": "Hello"}]
        
        logger.warning("Simulating complete model failure")
        response = manager.generate_completion(messages)
        
        self.assertIsNone(response)
        self.assertEqual(mock_post.call_count, len(manager.model_status))
        self.assertFalse(any(manager.model_status.values()))
        logger.error("All models failed as expected")


if __name__ == "__main__":
    unittest.main()