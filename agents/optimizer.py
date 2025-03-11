"""
Optimizer Agent for NeuroPrompt.
Refines prompts based on critique feedback using reinforcement learning concepts.
"""
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from crewai import Agent
from crewai.tools import BaseTool
from pydantic import Field

# Import custom logger
from core.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

class OptimizerTool(BaseTool):
    """Tool for optimizing prompts based on feedback."""
    
    name: str = "optimize_prompt"
    description: str = "Refines prompts based on critique feedback using reinforcement learning concepts"
    agent: Any = Field(description="The OptimizerAgent instance")
    
    def _run(self, prompt: str, critique: str) -> str:
        """
        Execute the prompt optimization.
        
        Args:
            prompt: The prompt to optimize
            critique: The critique feedback
            
        Returns:
            str: The optimized prompt
        """
        return self.agent.optimize_prompt(prompt, critique)

class OptimizerAgent:
    """
    Agent responsible for optimizing prompts based on critique feedback.
    Uses reinforcement learning concepts to improve prompt quality.
    """
    
    def __init__(self, model: str):
        """
        Initialize the Optimizer Agent.
        
        Args:
            model: The model ID to use for this agent
        """
        self.model = model
        self.optimization_history = self._load_optimization_history()
        logger.info(f"OptimizerAgent initialized with model: {model}")
    
    def _load_optimization_history(self) -> Dict[str, Any]:
        """
        Load prompt optimization history from file or initialize a new one.
        
        Returns:
            Dict[str, Any]: Optimization history data
        """
        history_path = "data/optimization_history.json"
        
        # Default history structure
        default_history = {
            "optimizations": [],
            "performance_metrics": {
                "avg_improvement_score": 0,
                "total_optimizations": 0,
                "frameworks": {}
            },
            "learning_params": {
                "learning_rate": 0.1,
                "exploration_rate": 0.2,
                "discount_factor": 0.9
            }
        }
        
        # Try to load history from file
        if os.path.exists(history_path):
            try:
                with open(history_path, "r") as f:
                    history = json.load(f)
                logger.info(f"Loaded optimization history from {history_path}")
                return history
            except Exception as e:
                logger.error(f"Error loading optimization history: {str(e)}")
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save default history
        try:
            with open(history_path, "w") as f:
                json.dump(default_history, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving default optimization history: {str(e)}")
            
        return default_history
    
    def _update_optimization_history(self, 
                                    original_prompt: str, 
                                    optimized_prompt: str, 
                                    critique: str, 
                                    improvement_score: float) -> None:
        """
        Update the optimization history with a new entry.
        
        Args:
            original_prompt: The original prompt
            optimized_prompt: The optimized prompt
            critique: The critique that guided the optimization
            improvement_score: Estimated improvement score (0-1)
        """
        # Extract framework if available
        framework = "unknown"
        if "Generated using" in original_prompt:
            framework_line = original_prompt.split("Generated using")[1].split("\n")[0]
            framework = framework_line.strip().replace("framework", "").strip()
        
        # Create new entry
        new_entry = {
            "timestamp": datetime.now().isoformat(),
            "framework": framework,
            "improvement_score": improvement_score,
            "critique_summary": critique[:200] + "..." if len(critique) > 200 else critique
        }
        
        # Update history
        self.optimization_history["optimizations"].append(new_entry)
        self.optimization_history["performance_metrics"]["total_optimizations"] += 1
        
        # Update average improvement score
        total_score = sum(entry["improvement_score"] for entry in self.optimization_history["optimizations"])
        avg_score = total_score / len(self.optimization_history["optimizations"])
        self.optimization_history["performance_metrics"]["avg_improvement_score"] = avg_score
        
        # Update framework-specific metrics
        if framework not in self.optimization_history["performance_metrics"]["frameworks"]:
            self.optimization_history["performance_metrics"]["frameworks"][framework] = {
                "count": 0,
                "avg_improvement": 0
            }
            
        framework_data = self.optimization_history["performance_metrics"]["frameworks"][framework]
        framework_data["count"] += 1
        
        # Update framework average improvement
        framework_entries = [entry for entry in self.optimization_history["optimizations"] 
                           if entry["framework"] == framework]
        framework_score = sum(entry["improvement_score"] for entry in framework_entries)
        framework_avg = framework_score / len(framework_entries)
        framework_data["avg_improvement"] = framework_avg
        
        # Save updated history
        try:
            with open("data/optimization_history.json", "w") as f:
                json.dump(self.optimization_history, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving optimization history: {str(e)}")
    
    def _apply_reinforcement_learning(self, framework: str) -> Dict[str, float]:
        """
        Apply reinforcement learning to adjust optimization parameters.
        
        Args:
            framework: The prompt framework being optimized
            
        Returns:
            Dict[str, float]: Updated learning parameters
        """
        # Get current learning parameters
        params = self.optimization_history["learning_params"]
        
        # This is a simplified RL implementation
        # In a production system, this would be more sophisticated
        
        # Adjust exploration rate based on performance
        if framework in self.optimization_history["performance_metrics"]["frameworks"]:
            framework_data = self.optimization_history["performance_metrics"]["frameworks"][framework]
            
            # If we have good performance, reduce exploration (exploit more)
            if framework_data["avg_improvement"] > 0.7:
                params["exploration_rate"] = max(0.05, params["exploration_rate"] * 0.9)
            # If performance is poor, increase exploration
            elif framework_data["avg_improvement"] < 0.3:
                params["exploration_rate"] = min(0.5, params["exploration_rate"] * 1.1)
        
        # Adjust learning rate based on total optimizations
        total_opts = self.optimization_history["performance_metrics"]["total_optimizations"]
        if total_opts > 50:
            # Decrease learning rate as we gain more experience
            params["learning_rate"] = max(0.01, params["learning_rate"] * 0.95)
        
        # Save updated parameters
        self.optimization_history["learning_params"] = params
        try:
            with open("data/optimization_history.json", "w") as f:
                json.dump(self.optimization_history, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving updated learning parameters: {str(e)}")
            
        return params
    
    def get_agent(self) -> Agent:
        """
        Create and return the CrewAI agent.
        
        Returns:
            Agent: The configured CrewAI agent
        """
        tool = OptimizerTool(agent=self)
        return Agent(
            role="Prompt Optimizer",
            goal="Refine and enhance prompts based on feedback",
            backstory="""You are an expert in prompt optimization, using advanced techniques 
            to refine prompts based on critique feedback. You understand how to balance 
            different aspects of prompt quality to achieve optimal results.""",
            allow_delegation=True,
            verbose=True,
            llm="openrouter/anthropic/claude-3-haiku:free",
            tools=[tool]
        )
    
    def optimize_prompt(self, prompt: str, critique: str) -> str:
        """
        Tool function to optimize a prompt based on critique feedback.
        
        Args:
            prompt: The original prompt to optimize
            critique: The critique with improvement suggestions
            
        Returns:
            str: The optimized prompt
        """
        logger.info(f"Optimizing prompt based on critique: {critique[:50]}...")
        
        # Extract framework if available
        framework = "unknown"
        if "Generated using" in prompt:
            framework_line = prompt.split("Generated using")[1].split("\n")[0]
            framework = framework_line.strip().replace("framework", "").strip()
        
        # Apply reinforcement learning to adjust parameters
        learning_params = self._apply_reinforcement_learning(framework)
        
        # Extract optimization targets from critique
        # In a real system, this would be more sophisticated
        optimization_targets = []
        
        # Simple extraction of improvement suggestions
        if "Improvement Suggestions" in critique:
            suggestions_section = critique.split("Improvement Suggestions")[1].split("##")[0]
            suggestions = [line.strip() for line in suggestions_section.split("\n") if line.strip() and ":" in line]
            optimization_targets.extend(suggestions)
        
        # Rewrite suggestions
        if "Suggested Rewrites" in critique:
            rewrites_section = critique.split("Suggested Rewrites")[1].split("##")[0]
            rewrites = [section for section in rewrites_section.split("###") if section.strip()]
            
            for rewrite in rewrites:
                if "Original:" in rewrite and "Suggested Rewrite:" in rewrite:
                    section_name = rewrite.split("\n")[0].strip()
                    optimization_targets.append(f"Rewrite {section_name} section")
        
        # If no targets were found, add generic ones
        if not optimization_targets:
            optimization_targets = [
                "Improve clarity and specificity",
                "Add more detailed examples",
                "Enhance structural organization",
                "Provide more context"
            ]
        
        logger.info(f"Identified {len(optimization_targets)} optimization targets")
        
        # In a real system, we would apply specific optimizations
        # For this example, we'll simulate the optimization process
        
        # Parse original prompt sections
        sections = {}
        current_section = "header"
        sections[current_section] = []
        
        for line in prompt.split("\n"):
            # Check if this is a section header
            if line.startswith("**") and ":**" in line:
                current_section = line.split(":**")[0].replace("**", "").strip()
                sections[current_section] = [line]
            else:
                if current_section in sections:
                    sections[current_section].append(line)
                else:
                    sections["misc"].append(line)
        
        # Apply suggested rewrites (simulated)
        if "Perspective" in sections and "Suggested Rewrite:" in critique and "Perspective Section" in critique:
            # Extract suggested rewrite
            rewrite_section = critique.split("Perspective Section")[1].split("###")[0]
            if "```" in rewrite_section:
                suggested_rewrite = rewrite_section.split("```")[1].strip()
                # Replace the original line with the suggested rewrite
                sections["Perspective"] = [suggested_rewrite]
        
        if "Situation" in sections and "Suggested Rewrite:" in critique and "Situation Section" in critique:
            # Extract suggested rewrite
            rewrite_section = critique.split("Situation Section")[1].split("###")[0]
            if "```" in rewrite_section:
                suggested_rewrite = rewrite_section.split("```")[1].strip()
                # Replace the original line with the suggested rewrite
                sections["Situation"] = [suggested_rewrite]
        
        # Reconstruct the prompt with optimizations
        optimized_sections = []
        
        # Add header if present
        if "header" in sections:
            optimized_sections.extend(sections["header"])
        
        # Add each section
        for section_name, section_lines in sections.items():
            if section_name != "header" and section_name != "footer":
                optimized_sections.extend(section_lines)
        
        # Add enhanced examples section if needed
        if "enhance examples" in str(optimization_targets).lower() and "Example" not in sections:
            optimized_sections.append("\n**Examples:**")
            optimized_sections.append("Here are some examples to illustrate the expected output:")
            optimized_sections.append("1. Example input: [Specific input example]")
            optimized_sections.append("   Example output: [Detailed output example]")
            optimized_sections.append("2. Example input: [Alternative input example]")
            optimized_sections.append("   Example output: [Alternative output example]")
        
        # Add footer with metadata
        footer = "\n\n---"
        if "Generated using" in prompt:
            # Preserve the original framework info
            for line in prompt.split("\n"):
                if "Generated using" in line:
                    footer += f"\n{line}"
                    break
        else:
            footer += f"\nGenerated using {framework} framework"
            
        # Add optimization info
        footer += f"\nOptimized using RL techniques (learning_rate={learning_params['learning_rate']:.2f}, exploration_rate={learning_params['exploration_rate']:.2f})"
        footer += f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        optimized_sections.append(footer)
        
        # Join all sections
        optimized_prompt = "\n".join(optimized_sections)
        
        # Calculate improvement score (simulated)
        # In a real system, this would be based on actual metrics
        improvement_score = 0.65  # Range: 0.0-1.0
        
        # Update optimization history
        self._update_optimization_history(prompt, optimized_prompt, critique, improvement_score)
        
        return optimized_prompt