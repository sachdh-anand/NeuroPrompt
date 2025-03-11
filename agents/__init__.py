"""
Agents module for NeuroPrompt.
Contains the specialized CrewAI agents for the system.
"""

from agents.prompt_generator import PromptGeneratorAgent
from agents.researcher import ResearcherAgent
from agents.critic import CriticAgent
from agents.optimizer import OptimizerAgent

__all__ = ['PromptGeneratorAgent', 'ResearcherAgent', 'CriticAgent', 'OptimizerAgent']