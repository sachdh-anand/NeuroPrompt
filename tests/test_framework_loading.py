"""
Test the framework loading functionality.
"""
import os
import sys
import unittest
from unittest.mock import patch, mock_open, MagicMock

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the PromptGeneratorAgent to test framework loading
from agents.prompt_generator import PromptGeneratorAgent, PromptFramework
from core.logger import get_logger

# Initialize logger
logger = get_logger(__name__)


class TestFrameworkLoading(unittest.TestCase):
    """Test cases for framework loading."""

    def setUp(self):
        """Set up test fixtures."""
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Create frameworks directory if it doesn't exist
        os.makedirs("documents/frameworks", exist_ok=True)
        
        logger.info("Test environment setup completed")
        
    def test_load_frameworks_from_defaults(self):
        """Test loading default frameworks when no files exist."""
        logger.info("Testing default framework loading")
        with patch('os.listdir', return_value=[]):
            generator = PromptGeneratorAgent(model="test-model")
            frameworks = generator.frameworks
            
            # Check that default frameworks were loaded
            self.assertIn("PECRA", frameworks)
            self.assertIn("SCQA", frameworks)
            self.assertIn("ReAct", frameworks)
            self.assertIn("RTF", frameworks)
            self.assertIn("RISEN", frameworks)
            
            # Check framework structure
            self.assertIsInstance(frameworks["PECRA"], PromptFramework)
            self.assertIsInstance(frameworks["PECRA"].structure, list)
            self.assertIsInstance(frameworks["PECRA"].best_for, list)
            self.assertTrue(len(frameworks["PECRA"].structure) > 0)
            
            logger.info("Default framework loading test completed")
            
    @patch('builtins.open')
    @patch('os.listdir')
    def test_load_frameworks_from_files(self, mock_listdir, mock_open_func):
        """Test loading frameworks from files."""
        logger.info("Testing framework loading from files")
        # Mock framework files
        mock_listdir.return_value = ["PECRA.md", "Custom.md"]
        
        # Mock file content for PECRA.md
        pecra_content = """# PECRA Framework

## Description
Test description for PECRA

## Structure
- item 1
- item 2

## Best For
- Best for item 1
- Best for item 2

## Example
Example content
"""
        
        # Mock file content for Custom.md
        custom_content = """# Custom Framework

## Description
Test description for Custom framework

## Structure
- Custom structure 1
- Custom structure 2

## Best For
- Custom best for 1
- Custom best for 2

## Example
Custom example
"""
        
        # Set up mock open to return different content for different files
        mock_file_cm = MagicMock()
        mock_file = MagicMock()
        mock_file_cm.__enter__.return_value = mock_file
        
        def side_effect(filename, *args, **kwargs):
            if "PECRA.md" in filename:
                mock_file.read.return_value = pecra_content
            elif "Custom.md" in filename:
                mock_file.read.return_value = custom_content
            return mock_file_cm
        
        mock_open_func.side_effect = side_effect
        
        # Test framework loading
        generator = PromptGeneratorAgent(model="test-model")
        frameworks = generator.frameworks
        
        # Check that frameworks were loaded from files
        self.assertIn("PECRA", frameworks)
        self.assertIn("Custom", frameworks)
        
        # Check content of loaded frameworks
        self.assertEqual(frameworks["PECRA"].description, "Test description for PECRA")
        self.assertEqual(frameworks["Custom"].description, "Test description for Custom framework")
        
        # Check structure was parsed correctly
        self.assertEqual(len(frameworks["PECRA"].structure), 2)
        self.assertEqual(frameworks["PECRA"].structure[0], "item 1")
        
        # Check best_for was parsed correctly
        self.assertEqual(len(frameworks["Custom"].best_for), 2)
        self.assertEqual(frameworks["Custom"].best_for[0], "Custom best for 1")
        
        logger.info("Framework loading from files test completed")
        
    def test_framework_selection(self):
        """Test framework selection logic."""
        logger.info("Testing framework selection logic")
        generator = PromptGeneratorAgent(model="test-model")
        
        # Test explicit mentions
        self.assertEqual(
            generator._select_best_framework("I want to use the PECRA framework for this"),
            "PECRA"
        )
        
        # Test keyword matching
        self.assertEqual(
            generator._select_best_framework("I have a problem with my website"),
            "SCQA"  # This matches the actual implementation which uses SCQA for problem-related queries
        )
        
        # Test steps/guide keywords
        self.assertEqual(
            generator._select_best_framework("I need steps to implement this"),
            "RISEN"
        )
        
        # Test reasoning keywords
        self.assertEqual(
            generator._select_best_framework("Help me think through this logically"),
            "ReAct"
        )
        
        # Test feedback/iteration keywords
        self.assertEqual(
            generator._select_best_framework("I need to improve this content"),
            "RTF"
        )
        
        # Test default case
        self.assertEqual(
            generator._select_best_framework("Just a regular request"),
            "PECRA"
        )
        
        logger.info("Framework selection test completed")


if __name__ == "__main__":
    unittest.main()