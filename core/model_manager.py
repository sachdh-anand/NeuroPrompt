"""
Model Manager for handling OpenRouter API and model selection.
"""
import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv
from core.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

# Load environment variables
load_dotenv()

class ModelManager:
    """
    Handles OpenRouter API interactions and model management.
    """
    
    def __init__(self):
        """Initialize the ModelManager with API key and model from environment variables."""
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
            
        # Use the model specified in .env
        self.model = os.getenv("OPENROUTER_MODEL_ID", "anthropic/claude-3-haiku:free")
        
        # API endpoint
        self.api_endpoint = "https://openrouter.ai/api/v1/chat/completions"
            
        logger.info(f"ModelManager initialized with model: {self.model}")
    
    def get_available_model(self) -> str:
        """
        Returns the configured model.
        
        Returns:
            str: The model ID to use
        """
        return self.model
    
    def generate_completion(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Generate a completion using OpenRouter API.
        
        Args:
            prompt: The input prompt
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            str: The completion text
            
        Raises:
            Exception: If completion fails
        """
        logger.info(f"Generating completion with model: {self.model}")
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://neuroprompt.example.com",  # Use your actual domain in production
                "X-Title": "NeuroPrompt"
            }
            
            data = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "route": "fallback"  # This tells OpenRouter to automatically try other options if needed
            }
            
            response = requests.post(
                self.api_endpoint,
                headers=headers,
                json=data,
                timeout=60  # Set a reasonable timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                logger.info(f"Completion successful with {self.model}")
                return content
            else:
                error_msg = f"API request failed with status code {response.status_code}: {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)
                
        except Exception as e:
            error_msg = f"Error generating completion with {self.model}: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)