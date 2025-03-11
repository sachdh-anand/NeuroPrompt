"""
Critic Agent for NeuroPrompt.
Reviews and critiques generated prompts to improve their effectiveness.
"""
import os
import json
from typing import Dict, List, Any, Optional
from crewai import Agent
from crewai.tools import BaseTool
from pydantic import Field

# Import custom logger
from core.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

class CriticTool(BaseTool):
    """Tool for critiquing generated prompts."""
    
    name: str = "critique_prompt"
    description: str = "Reviews and critiques generated prompts to improve their effectiveness"
    agent: Any = Field(description="The CriticAgent instance")
    
    def _run(self, prompt: str) -> Dict[str, Any]:
        """
        Execute the prompt critique.
        
        Args:
            prompt: The prompt to critique
            
        Returns:
            Dict[str, Any]: The critique results
        """
        return self.agent.critique_prompt(prompt)

class CriticAgent:
    """
    Agent responsible for reviewing and critiquing generated prompts.
    """
    
    def __init__(self, model: str):
        """
        Initialize the Critic Agent.
        
        Args:
            model: The model ID to use for this agent
        """
        self.model = model
        self.evaluation_criteria = self._load_evaluation_criteria()
        logger.info(f"CriticAgent initialized with model: {model}")
    
    def _load_evaluation_criteria(self) -> Dict[str, Dict[str, Any]]:
        """
        Load prompt evaluation criteria from file or use defaults.
        
        Returns:
            Dict[str, Dict[str, Any]]: Dictionary of evaluation criteria
        """
        # Default evaluation criteria
        default_criteria = {
            "clarity": {
                "description": "Is the prompt clear and unambiguous?",
                "evaluation_questions": [
                    "Are the instructions clearly stated?",
                    "Is there any ambiguity in what is being requested?",
                    "Are key terms well-defined?",
                    "Does the prompt use precise language?"
                ],
                "weight": 0.25
            },
            "specificity": {
                "description": "Is the prompt specific enough to generate the desired response?",
                "evaluation_questions": [
                    "Does the prompt clearly specify the expected output format?",
                    "Are there specific requirements or constraints mentioned?",
                    "Does the prompt include enough detail for accurate generation?",
                    "Is the scope of the request clearly defined?"
                ],
                "weight": 0.20
            },
            "context": {
                "description": "Does the prompt provide adequate context?",
                "evaluation_questions": [
                    "Is there sufficient background information?",
                    "Does the prompt establish the proper framing?",
                    "Is there a clear perspective or role defined?",
                    "Does the context align with the request?"
                ],
                "weight": 0.15
            },
            "structure": {
                "description": "Is the prompt well-structured and organized?",
                "evaluation_questions": [
                    "Is the prompt organized in a logical sequence?",
                    "Are different components clearly separated?",
                    "Is the prompt formatted for easy reading?",
                    "Does the structure support the intent of the prompt?"
                ],
                "weight": 0.15
            },
            "completeness": {
                "description": "Is the prompt complete with all necessary elements?",
                "evaluation_questions": [
                    "Does the prompt include all required components based on its framework?",
                    "Are all relevant parameters specified?",
                    "Does the prompt address potential edge cases?",
                    "Are examples included where appropriate?"
                ],
                "weight": 0.15
            },
            "effectiveness": {
                "description": "Is the prompt likely to be effective for its intended purpose?",
                "evaluation_questions": [
                    "Will the prompt likely generate the intended response?",
                    "Is the prompt optimized for the specific task?",
                    "Does the prompt use the most appropriate techniques?",
                    "Is the prompt aligned with best practices for its use case?"
                ],
                "weight": 0.10
            }
        }
        
        # Try to load criteria from file
        criteria_path = "data/evaluation_criteria.json"
        if os.path.exists(criteria_path):
            try:
                with open(criteria_path, "r") as f:
                    criteria = json.load(f)
                logger.info(f"Loaded evaluation criteria from {criteria_path}")
                return criteria
            except Exception as e:
                logger.error(f"Error loading evaluation criteria: {str(e)}")
        
        # Save default criteria for future use
        try:
            os.makedirs("data", exist_ok=True)
            with open(criteria_path, "w") as f:
                json.dump(default_criteria, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving default evaluation criteria: {str(e)}")
            
        return default_criteria
    
    def get_agent(self) -> Agent:
        """
        Create and return the CrewAI agent.
        
        Returns:
            Agent: The configured CrewAI agent
        """
        tool = CriticTool(agent=self)
        return Agent(
            role="Prompt Critic",
            goal="Review and improve prompt effectiveness",
            backstory="""You are an expert prompt critic with deep understanding of what 
            makes prompts effective. You analyze prompts based on clarity, specificity, 
            context, and other key factors to ensure they achieve their intended goals.""",
            allow_delegation=True,
            verbose=True,
            llm="openrouter/anthropic/claude-3-haiku:free",
            tools=[tool]
        )
    
    def critique_prompt(self, prompt: str) -> str:
        """
        Tool function to critique a generated prompt.
        
        Args:
            prompt: The prompt to critique
            
        Returns:
            str: Detailed critique with improvement suggestions
        """
        logger.info(f"Critiquing prompt: {prompt[:50]}...")
        
        # Extract framework name if present
        framework = "unknown"
        if "Generated using" in prompt:
            framework_line = prompt.split("Generated using")[1].split("\n")[0]
            framework = framework_line.strip().replace("framework", "").strip()
        
        # Initialize critique sections
        critique_sections = [
            "# Prompt Critique\n",
            f"## Framework: {framework}\n"
        ]
        
        # Overall impression (placeholder - in a real system, this would be generated)
        critique_sections.append("## Overall Impression\n")
        critique_sections.append("The prompt follows the specified framework structure and addresses the core requirements. However, there are areas for improvement in clarity, specificity, and effectiveness.")
        
        # Detailed critique for each criterion
        critique_sections.append("\n## Detailed Evaluation\n")
        
        total_score = 0
        for criterion_name, criterion_data in self.evaluation_criteria.items():
            # In a real system, this would contain actual evaluation logic
            # For this example, we'll use predefined feedback
            
            # Score each criterion (simulated)
            score = 0
            if criterion_name == "clarity":
                score = 3.5  # Out of 5
                feedback = [
                    "Instructions are generally clear, but could benefit from more precise language in sections.",
                    "There is some ambiguity in what specific outputs are expected.",
                    "Consider adding clearer definitions for technical terms used."
                ]
            elif criterion_name == "specificity":
                score = 3.0  # Out of 5
                feedback = [
                    "The output format could be more explicitly defined.",
                    "More specific examples would help clarify expectations.",
                    "Consider adding quantitative parameters where applicable."
                ]
            elif criterion_name == "context":
                score = 4.0  # Out of 5
                feedback = [
                    "Good background information is provided.",
                    "The role/perspective is well-established.",
                    "Consider adding more domain-specific context."
                ]
            elif criterion_name == "structure":
                score = 4.5  # Out of 5
                feedback = [
                    "The prompt has excellent logical organization.",
                    "Different components are clearly separated.",
                    "Formatting enhances readability."
                ]
            elif criterion_name == "completeness":
                score = 3.5  # Out of 5
                feedback = [
                    "Most required components are present.",
                    "Could benefit from addressing potential edge cases.",
                    "Consider adding more illustrative examples."
                ]
            elif criterion_name == "effectiveness":
                score = 3.8  # Out of 5
                feedback = [
                    "The prompt is likely to generate good results for the intended purpose.",
                    "Consider incorporating more domain-specific techniques.",
                    "Align more closely with best practices for this specific use case."
                ]
            
            # Calculate weighted score
            weighted_score = score * criterion_data["weight"]
            total_score += weighted_score
            
            # Add to critique
            critique_sections.append(f"### {criterion_name.capitalize()} (Score: {score}/5)\n")
            critique_sections.append(f"{criterion_data['description']}\n")
            critique_sections.append("**Feedback:**\n")
            for item in feedback:
                critique_sections.append(f"- {item}\n")
            critique_sections.append("\n")
        
        # Calculate overall score
        overall_score = total_score * 20  # Convert to 0-100 scale
        critique_sections.append(f"## Overall Score: {overall_score:.1f}/100\n")
        
        # Specific improvement suggestions
        critique_sections.append("## Improvement Suggestions\n")
        critique_sections.append("1. **Enhance Clarity**: Use more precise language and clearly define expected outputs.\n")
        critique_sections.append("2. **Increase Specificity**: Add more detailed examples and explicit parameters.\n")
        critique_sections.append("3. **Expand Context**: Include more domain-specific information relevant to the task.\n")
        critique_sections.append("4. **Address Edge Cases**: Consider potential variations or exceptions in the request.\n")
        critique_sections.append("5. **Optimize for Target Model**: Adjust the prompt structure to better leverage the capabilities of the target AI model.\n")
        
        # Rewritten sections
        critique_sections.append("## Suggested Rewrites\n")
        
        # Simulate finding sections to rewrite
        if "Perspective:" in prompt and framework == "PECRA":
            critique_sections.append("### Perspective Section\n")
            critique_sections.append("**Original:**\n")
            
            # Extract original section (simplified)
            original_section = "Perspective: You are an AI assistant with expertise in this subject"
            for line in prompt.split("\n"):
                if line.startswith("**Perspective:**"):
                    original_section = line
                    break
            
            critique_sections.append(f"```\n{original_section}\n```\n")
            critique_sections.append("**Suggested Rewrite:**\n")
            critique_sections.append("```\n**Perspective:** You are a senior AI specialist with deep expertise in prompt engineering and optimization, with particular focus on [specific domain] applications\n```\n")
            critique_sections.append("This provides more specific expertise and establishes greater authority.\n")
        
        elif "Situation:" in prompt and framework == "SCQA":
            critique_sections.append("### Situation Section\n")
            critique_sections.append("**Original:**\n")
            
            # Extract original section (simplified)
            original_section = "Situation: The current state is standard/neutral"
            for line in prompt.split("\n"):
                if line.startswith("**Situation:**"):
                    original_section = line
                    break
            
            critique_sections.append(f"```\n{original_section}\n```\n")
            critique_sections.append("**Suggested Rewrite:**\n")
            critique_sections.append("```\n**Situation:** The current process is inefficient and time-consuming, resulting in [specific measurable impact]\n```\n")
            critique_sections.append("This creates a more compelling situation with concrete details.\n")
        
        # Final summary
        critique_sections.append("## Summary\n")
        critique_sections.append("The prompt has a solid foundation following the appropriate framework, but would benefit from increased specificity, clearer expectations, and more contextual relevance. Implementing the suggested improvements would likely increase its effectiveness significantly.\n")
        
        # Join all sections
        final_critique = "\n".join(critique_sections)
        
        return final_critique