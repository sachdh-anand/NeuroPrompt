"""
Model Manager for handling OpenRouter API and model selection/fallback.
"""
import os
import requests
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/execution.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("model_manager")

# Load environment variables
load_dotenv()

class ModelManager:
    """
    Handles OpenRouter API interactions, model selection, and fallback mechanisms.
    """
    
    def __init__(self):
        """Initialize the ModelManager with API key and models from environment variables."""
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
            
        self.primary_model = os.getenv("OPENROUTER_MODEL_ID", "deepseek/deepseek-r1:free")
        
        # Get fallback models from environment variables
        fallback_models_str = os.getenv("OPENROUTER_FALLBACK_MODELS", 
                                        "google/gemini-2.0-pro-exp-02-05:free,google/gemini-2.0-flash-exp:free,deepseek/deepseek-chat:free")
        self.fallback_models = fallback_models_str.split(",")
        
        # API endpoint
        self.api_endpoint = "https://openrouter.ai/api/v1/chat/completions"
        
        # Track model availability
        self.model_status = {self.primary_model: True}
        for model in self.fallback_models:
            self.model_status[model] = True
            
        logger.info(f"ModelManager initialized with primary model: {self.primary_model}")
        logger.info(f"Fallback models: {self.fallback_models}")
    
    def get_available_model(self) -> str:
        """
        Returns the first available model (primary if available, otherwise first available fallback).
        
        Returns:
            str: The model ID to use
        """
        if self.model_status[self.primary_model]:
            return self.primary_model
            
        for model in self.fallback_models:
            if self.model_status[model]:
                logger.info(f"Using fallback model: {model}")
                return model
                
        # If we get here, reset all models to available and try the primary again
        logger.warning("All models marked as unavailable. Resetting status and trying primary model.")
        for model in self.model_status:
            self.model_status[model] = True
            
        return self.primary_model
    
    def generate_completion(self, messages: List[Dict[str, str]], 
                            temperature: float = 0.7,
                            max_tokens: int = 1000) -> Optional[Dict[str, Any]]:
        """
        Generate a completion using OpenRouter API with automatic fallback.
        
        Args:
            messages: List of message dictionaries (role and content)
            temperature: Sampling temperature (default: 0.7)
            max_tokens: Maximum tokens to generate (default: 1000)
            
        Returns:
            Optional[Dict[str, Any]]: The API response or None if all models fail
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Try models until one works or we run out of options
        for _ in range(len(self.model_status)):
            model = self.get_available_model()
            
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            try:
                logger.info(f"Sending request to OpenRouter with model: {model}")
                response = requests.post(self.api_endpoint, json=payload, headers=headers)
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Error with model {model}: {str(e)}")
                # Mark this model as unavailable
                self.model_status[model] = False
                
        logger.error("All models failed. Unable to generate completion.")
        return None

    def get_models_status(self) -> Dict[str, bool]:
        """
        Returns the current status of all models.
        
        Returns:
            Dict[str, bool]: Dictionary of model IDs and their availability status
        """
        return self.model_status
        
    def reset_model_status(self) -> None:
        """Reset the status of all models to available."""
        for model in self.model_status:
            self.model_status[model] = True
        logger.info("Reset status of all models to available")