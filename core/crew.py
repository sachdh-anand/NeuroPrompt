"""
Main CrewAI Orchestration module for NeuroPrompt.
"""
import os
from typing import Dict, List, Any
from crewai import Crew, Agent, Task
from dotenv import load_dotenv
from core.model_manager import ModelManager
from core.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

# Load environment variables
load_dotenv()

class NeuroPromptCrew:
    """
    Orchestrates the CrewAI agents for the NeuroPrompt system.
    """
    
    def __init__(self):
        """Initialize the NeuroPrompt Crew with necessary agents and model manager."""
        logger.info("Initializing NeuroPromptCrew")
        
        # Initialize model manager
        self.model_manager = ModelManager()
        
        # Placeholder for agents (will be initialized on demand)
        self.prompt_generator = None
        self.researcher = None
        self.critic = None
        self.optimizer = None
        
        # Initialize crew
        self.crew = None
        
    def _initialize_agents(self):
        """Initialize all agents if they haven't been initialized yet."""
        # Import agent classes here to avoid circular imports
        from agents.prompt_generator import PromptGeneratorAgent
        from agents.researcher import ResearcherAgent
        from agents.critic import CriticAgent
        from agents.optimizer import OptimizerAgent
        
        logger.info("Initializing CrewAI agents")
        
        # Initialize the model
        model = self.model_manager.get_available_model()
        
        # Initialize agents with the model
        self.prompt_generator = PromptGeneratorAgent(model=model).get_agent()
        self.researcher = ResearcherAgent(model=model).get_agent()
        self.critic = CriticAgent(model=model).get_agent()
        self.optimizer = OptimizerAgent(model=model).get_agent()
    
    def _create_crew(self, user_input: str) -> Crew:
        """
        Create the CrewAI crew with all necessary tasks.
        
        Args:
            user_input: User's prompt request
            
        Returns:
            Crew: Configured CrewAI crew
        """
        self._initialize_agents()
        
        # Create tasks with proper context
        research_task = Task(
            description=f"Research the latest prompt engineering techniques and frameworks that would be relevant for this user request: '{user_input}'",
            expected_output="A comprehensive summary of the most relevant prompt engineering techniques and frameworks for this specific user request.",
            agent=self.researcher
        )
        
        generate_task = Task(
            description=f"Generate an optimized prompt based on the research and this user request: '{user_input}'",
            expected_output="A well-structured prompt that addresses the user's needs using the appropriate framework.",
            agent=self.prompt_generator,
            output_file="data/generated_prompt.txt",
            dependencies=[research_task]
        )
        
        critique_task = Task(
            description="Critique the generated prompt for effectiveness, clarity, and optimization potential.",
            expected_output="A detailed critique with specific improvement suggestions for the prompt.",
            agent=self.critic,
            output_file="data/prompt_critique.txt",
            dependencies=[generate_task]
        )
        
        optimize_task = Task(
            description="Optimize the prompt based on the critique feedback.",
            expected_output="The final optimized prompt with all improvements applied.",
            agent=self.optimizer,
            output_file="data/final_prompt.txt",
            dependencies=[generate_task, critique_task]
        )
        
        # Create crew
        crew = Crew(
            agents=[self.prompt_generator, self.researcher, self.critic, self.optimizer],
            tasks=[research_task, generate_task, critique_task, optimize_task],
            verbose=True
        )
        
        return crew
    
    def generate_prompt(self, user_input: str) -> Dict[str, Any]:
        """
        Generate an optimized prompt based on user input.
        
        Args:
            user_input: The user's prompt request
            
        Returns:
            Dict[str, Any]: Results including the final prompt
        """
        logger.info(f"Generating prompt for user input: {user_input}")
        
        # Ensure directories exist
        os.makedirs("data", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        
        # Create and run the crew
        crew = self._create_crew(user_input)
        result = crew.kickoff()
        
        # Read final prompt from file
        final_prompt = "Could not generate prompt"
        try:
            with open("data/final_prompt.txt", "r") as f:
                final_prompt = f.read()
        except FileNotFoundError:
            logger.error("Final prompt file not found")
        
        # Compile results
        results = {
            "user_input": user_input,
            "final_prompt": final_prompt,
            "process_info": result
        }
        
        return results