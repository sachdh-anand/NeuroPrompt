"""
Prompt Generator Agent for NeuroPrompt.
Analyzes user input and generates optimized prompts.
"""
import os
import json
import datetime
from typing import Dict, List, Any, Optional
from crewai import Agent
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

# Import custom logger
from core.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

class PromptGeneratorTool(BaseTool):
    """Tool for generating optimized prompts."""
    
    name: str = "generate_optimized_prompt"
    description: str = "Generates an optimized prompt based on user input and research data"
    agent: Any = Field(description="The PromptGeneratorAgent instance")
    
    def _run(self, user_input: str, research_output: str = "") -> str:
        """
        Execute the prompt generation.
        
        Args:
            user_input: The user's prompt request
            research_output: Research data from the researcher agent
            
        Returns:
            str: The generated optimized prompt
        """
        return self.agent.generate_optimized_prompt(user_input, research_output)

class PromptFramework(BaseModel):
    """Model for prompt engineering frameworks."""
    name: str
    description: str
    structure: List[str]
    best_for: List[str]
    example: str

class PromptGeneratorAgent:
    """
    Agent that generates optimized prompts based on user input and research.
    """
    
    def __init__(self, model: str):
        """
        Initialize the Prompt Generator Agent.
        
        Args:
            model: The model ID to use for this agent
        """
        self.model = model
        self.frameworks = self._load_frameworks()
        logger.info(f"PromptGeneratorAgent initialized with model: {model}")
        
    def _load_frameworks(self) -> Dict[str, PromptFramework]:
        """
        Load prompt engineering frameworks from documents folder.
        
        Returns:
            Dict[str, PromptFramework]: Dictionary of framework objects
        """
        frameworks = {}
        
        # Create framework directory if it doesn't exist
        os.makedirs("documents/frameworks", exist_ok=True)
        
        # Hardcoded frameworks as fallback if files don't exist
        default_frameworks = {
            "PECRA": PromptFramework(
                name="PECRA",
                description="Perspective, Experience, Context, Request, Action framework",
                structure=["Perspective: Define the role or perspective to adopt", 
                          "Experience: Specify relevant experience or expertise", 
                          "Context: Provide context or background information",
                          "Request: Clearly state what you want",
                          "Action: Specify the desired action or output format"],
                best_for=["Role-based tasks", "Expert consultations", "Complex outputs"],
                example="Perspective: You are a senior data scientist\nExperience: With 10+ years in predictive modeling\nContext: Working with a retail dataset of customer purchases\nRequest: Analyze purchase patterns\nAction: Provide actionable insights in bullet points"
            ),
            "SCQA": PromptFramework(
                name="SCQA",
                description="Situation, Complication, Question, Answer framework",
                structure=["Situation: Establish the current situation", 
                          "Complication: Identify the complication or problem", 
                          "Question: Formulate the key question to address",
                          "Answer: Guide towards the desired answer or output"],
                best_for=["Problem-solving prompts", "Business analyses", "Decision-making scenarios"],
                example="Situation: Our e-commerce site has stable traffic\nComplication: But conversion rates dropped 15% last month\nQuestion: What might be causing this decrease?\nAnswer: Provide 3-5 potential causes and solutions"
            ),
            "ReAct": PromptFramework(
                name="ReAct",
                description="Reasoning and Acting framework",
                structure=["Thought: Think step by step about the problem", 
                          "Action: Define what action to take based on reasoning", 
                          "Observation: Note what is observed from the action",
                          "Next thought/action: Continue the reasoning process"],
                best_for=["Complex reasoning tasks", "Multi-step problems", "Logical deductions"],
                example="I need to solve this math problem: (14 × 6) ÷ (3 + 5)\nThought: I need to follow order of operations (PEMDAS)\nAction: First, calculate what's in the parentheses: 3 + 5 = 8\nObservation: The expression is now (14 × 6) ÷ 8\nThought: Now I'll multiply 14 × 6\nAction: Calculate 14 × 6 = 84\nObservation: The expression is now 84 ÷ 8\nThought: Finally, I'll divide 84 by 8\nAction: Calculate 84 ÷ 8 = 10.5\nThe answer is 10.5"
            ),
            "RTF": PromptFramework(
                name="RTF",
                description="Rule of Three Feedback framework",
                structure=["Round 1: Initial prompt and response", 
                          "Feedback: Provide specific feedback on what needs improvement", 
                          "Round 2: Improved prompt based on feedback",
                          "Feedback: Second round of focused feedback",
                          "Round 3: Final optimized prompt"],
                best_for=["Iterative development", "Creative content", "Refining existing prompts"],
                example="Round 1: Write a short story about a detective\nFeedback: Make the detective more unique and add a surprising twist\nRound 2: Write a short story about a detective who can speak to buildings\nFeedback: Make the ending more satisfying\nRound 3: Write a short story about a detective who can speak to buildings, with a satisfying resolution to the case"
            ),
            "RISEN": PromptFramework(
                name="RISEN",
                description="Role, Information, Steps, Example, Negative example framework",
                structure=["Role: Clearly define the role being assigned", 
                          "Information: Provide all necessary context and data", 
                          "Steps: Outline specific steps to follow",
                          "Example: Show a positive example of desired output",
                          "Negative example: Demonstrate what to avoid"],
                best_for=["Detailed instructions", "Educational content", "Technical documentation"],
                example="Role: You are a technical documentation writer\nInformation: We're launching a new API for our payment system\nSteps: 1. Explain authentication process, 2. Detail each endpoint, 3. Provide code examples\nExample: Here's good API documentation: [example]\nNegative example: Avoid vague descriptions like this: [counter-example]"
            )
        }
        
        # Try to load frameworks from files
        framework_files = [f for f in os.listdir("documents/frameworks") if f.endswith(".md")]
        
        if framework_files:
            logger.info(f"Loading {len(framework_files)} frameworks from documents/frameworks")
            for file in framework_files:
                try:
                    with open(f"documents/frameworks/{file}", "r") as f:
                        content = f.read()
                        # Parse markdown to extract framework information
                        # This is a simplified version - in practice you'd use a proper markdown parser
                        name = file.replace(".md", "")
                        sections = content.split("## ")
                        
                        description = ""
                        structure = []
                        best_for = []
                        example = ""
                        
                        for section in sections:
                            if section.startswith("Description"):
                                description = section.replace("Description", "").strip()
                            elif section.startswith("Structure"):
                                structure_text = section.replace("Structure", "").strip()
                                structure = []
                                for line in structure_text.split("\n"):
                                    line = line.strip()
                                    if line and line != "-":
                                        # Remove any leading dash and space
                                        while line.startswith("-") or line.startswith(" "):
                                            line = line[1:]
                                        line = line.strip()
                                        if line:
                                            structure.append(line)
                            elif section.startswith("Best For"):
                                best_for_text = section.replace("Best For", "").strip()
                                best_for = []
                                for line in best_for_text.split("\n"):
                                    line = line.strip()
                                    if line and line != "-":
                                        # Remove any leading dash and space
                                        while line.startswith("-") or line.startswith(" "):
                                            line = line[1:]
                                        line = line.strip()
                                        if line:
                                            best_for.append(line)
                            elif section.startswith("Example"):
                                example = section.replace("Example", "").strip()
                        
                        frameworks[name] = PromptFramework(
                            name=name,
                            description=description,
                            structure=structure if structure else ["No structure defined"],
                            best_for=best_for if best_for else ["General purpose"],
                            example=example
                        )
                except Exception as e:
                    logger.error(f"Error loading framework from {file}: {str(e)}")
        
        # Fall back to default frameworks if none were loaded
        if not frameworks:
            logger.info("No frameworks found in files, using default frameworks")
            frameworks = default_frameworks
        
        # Save the knowledge graph of frameworks for reference
        try:
            os.makedirs("data", exist_ok=True)
            with open("data/knowledge_graph.json", "w") as f:
                json.dump({name: framework.model_dump() for name, framework in frameworks.items()}, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving knowledge graph: {str(e)}")
            
        return frameworks
    
    def _select_best_framework(self, user_input: str, research_data: str = "") -> str:
        """
        Select the best prompt engineering framework based on the user input and research.
        
        Args:
            user_input: The user's prompt request
            research_data: Research data from the researcher agent
            
        Returns:
            str: Name of the selected framework
        """
        # This is a simplified selection logic
        # In a full implementation, you would use semantic matching or ML to select the best framework
        
        # Check for explicit keywords in user input
        user_input_lower = user_input.lower()
        for name, framework in self.frameworks.items():
            if name.lower() in user_input_lower:
                logger.info(f"Selected {name} framework based on explicit mention")
                return name
                
        # Simple keyword matching (in a real implementation this would be more sophisticated)
        if "problem" in user_input_lower or "issue" in user_input_lower or "challenge" in user_input_lower:
            return "SCQA"
        elif "steps" in user_input_lower or "guide" in user_input_lower or "tutorial" in user_input_lower:
            return "RISEN"
        elif "reason" in user_input_lower or "think" in user_input_lower or "logic" in user_input_lower:
            return "ReAct"
        elif "improve" in user_input_lower or "feedback" in user_input_lower or "iterate" in user_input_lower:
            return "RTF"
        
        # Default to PECRA as it's versatile
        return "PECRA"
    
    def _generate_prompt_with_framework(self, 
                                       framework_name: str, 
                                       user_input: str, 
                                       research_data: str = "") -> str:
        """
        Generate a prompt using the selected framework.
        
        Args:
            framework_name: Name of the selected framework
            user_input: The user's prompt request
            research_data: Research data from the researcher agent
            
        Returns:
            str: Generated prompt
        """
        framework = self.frameworks.get(framework_name)
        if not framework:
            logger.error(f"Framework {framework_name} not found, falling back to PECRA")
            framework = self.frameworks.get("PECRA", self.frameworks[list(self.frameworks.keys())[0]])
            
        # Generate prompt based on framework structure
        # This is a simplified implementation - in practice, this would be more sophisticated
        prompt_sections = []
        
        if framework_name == "PECRA":
            # Perspective, Experience, Context, Request, Action
            prompt_sections.append(f"# Prompt using {framework_name} Framework\n")
            
            # Extract potential role from user input
            role = "an AI assistant with expertise in this subject"
            if "expert" in user_input.lower() or "specialist" in user_input.lower():
                # Extract expertise area
                words = user_input.split()
                for i, word in enumerate(words):
                    if word.lower() in ["expert", "specialist"]:
                        if i < len(words) - 2:
                            role = f"a {word} in {' '.join(words[i+1:i+3])}"
                            break
            
            prompt_sections.append(f"**Perspective:** You are {role}")
            prompt_sections.append("**Experience:** You have extensive knowledge of best practices and advanced techniques in this domain")
            
            # Extract context from user input and research
            context = user_input
            if research_data:
                context = f"{user_input}\n\nBased on recent research: {research_data}"
                
            prompt_sections.append(f"**Context:** {context}")
            prompt_sections.append(f"**Request:** {user_input}")
            prompt_sections.append("**Action:** Provide a comprehensive, well-structured response that directly addresses the request, using examples where appropriate")
            
        elif framework_name == "SCQA":
            # Situation, Complication, Question, Answer
            prompt_sections.append(f"# Prompt using {framework_name} Framework\n")
            
            # Simple situation extraction
            situation = "The current state is standard/neutral"
            if "currently" in user_input.lower():
                # Try to extract the current situation
                current_idx = user_input.lower().find("currently")
                if current_idx > 0:
                    end_idx = user_input.find(".", current_idx)
                    if end_idx > 0:
                        situation = user_input[current_idx:end_idx+1]
            
            prompt_sections.append(f"**Situation:** {situation}")
            
            # Extract complication
            complication = "A need has arisen requiring specialized knowledge or assistance"
            if "problem" in user_input.lower() or "issue" in user_input.lower() or "challenge" in user_input.lower():
                # Try to extract the problem
                problem_indicators = ["problem", "issue", "challenge"]
                for indicator in problem_indicators:
                    if indicator in user_input.lower():
                        indicator_idx = user_input.lower().find(indicator)
                        if indicator_idx > 0:
                            end_idx = user_input.find(".", indicator_idx)
                            if end_idx > 0:
                                complication = user_input[indicator_idx-20 if indicator_idx > 20 else 0:end_idx+1]
                                break
            
            prompt_sections.append(f"**Complication:** {complication}")
            prompt_sections.append(f"**Question:** {user_input}")
            prompt_sections.append("**Answer:** Provide a comprehensive analysis and solution that addresses the question directly")
            
        elif framework_name == "ReAct":
            # Reasoning and Acting
            prompt_sections.append(f"# Prompt using {framework_name} Framework\n")
            prompt_sections.append("You will solve this problem by thinking step-by-step:")
            prompt_sections.append(f"**Problem:** {user_input}")
            prompt_sections.append("**Approach:**")
            prompt_sections.append("1. **Thought:** First, think about the key aspects of this problem.")
            prompt_sections.append("2. **Action:** Identify what information or techniques are needed.")
            prompt_sections.append("3. **Observation:** Analyze the available information and constraints.")
            prompt_sections.append("4. **Thought:** Consider multiple approaches to solve the problem.")
            prompt_sections.append("5. **Action:** Select the most appropriate approach and implement it step by step.")
            prompt_sections.append("6. **Observation:** Evaluate the results of your approach.")
            prompt_sections.append("7. **Final Answer:** Provide the complete solution with explanation.")
            
        elif framework_name == "RISEN":
            # Role, Information, Steps, Example, Negative example
            prompt_sections.append(f"# Prompt using {framework_name} Framework\n")
            
            # Extract potential role from user input
            role = "an AI assistant with expertise in this subject"
            if "expert" in user_input.lower() or "specialist" in user_input.lower():
                # Extract expertise area
                words = user_input.split()
                for i, word in enumerate(words):
                    if word.lower() in ["expert", "specialist"]:
                        if i < len(words) - 2:
                            role = f"a {word} in {' '.join(words[i+1:i+3])}"
                            break
            
            prompt_sections.append(f"**Role:** You are {role}")
            
            # Information from user input and research
            information = user_input
            if research_data:
                information = f"{user_input}\n\nAdditional information: {research_data}"
                
            prompt_sections.append(f"**Information:** {information}")
            
            # Generic steps
            prompt_sections.append("**Steps:**")
            prompt_sections.append("1. Analyze the request thoroughly.")
            prompt_sections.append("2. Identify the key requirements and constraints.")
            prompt_sections.append("3. Develop a comprehensive response addressing all aspects.")
            prompt_sections.append("4. Format your response clearly with appropriate sections.")
            prompt_sections.append("5. Review for accuracy and completeness before submitting.")
            
            # Example and negative example would be more specific in a real implementation
            prompt_sections.append("**Example:** A thorough, well-structured response that fully addresses the request with clear organization and appropriate level of detail.")
            prompt_sections.append("**Negative Example:** A vague, disorganized response that misses key aspects of the request or provides excessive irrelevant information.")
            
        elif framework_name == "RTF":
            # Rule of Three Feedback
            prompt_sections.append(f"# Prompt using {framework_name} Framework\n")
            prompt_sections.append("We will use an iterative approach to generate the best response:")
            prompt_sections.append(f"**Initial Request:** {user_input}")
            prompt_sections.append("**Iteration Process:**")
            prompt_sections.append("1. Generate an initial response to the request.")
            prompt_sections.append("2. Critique your response, identifying areas for improvement in clarity, comprehensiveness, and effectiveness.")
            prompt_sections.append("3. Generate an improved response based on your critique.")
            prompt_sections.append("4. Perform a final review to ensure the response fully addresses the request and is optimized for clarity and usefulness.")
            prompt_sections.append("5. Provide your final, optimized response.")
            
        else:
            # Generic fallback prompt structure
            prompt_sections.append(f"# Using a custom approach based on {framework_name}\n")
            prompt_sections.append(f"**Request:** {user_input}")
            
            if research_data:
                prompt_sections.append(f"**Additional Context:** {research_data}")
                
            prompt_sections.append("**Instructions:**")
            prompt_sections.append("1. Analyze the request thoroughly")
            prompt_sections.append("2. Provide a comprehensive, well-structured response")
            prompt_sections.append("3. Include relevant examples or illustrations where appropriate")
            prompt_sections.append("4. Ensure your response is directly aligned with the user's needs")
            
        return "\n\n".join(prompt_sections)
    
    def get_agent(self) -> Agent:
        """
        Create and return the CrewAI agent.
        
        Returns:
            Agent: The configured CrewAI agent
        """
        tool = PromptGeneratorTool(agent=self)
        return Agent(
            role="Prompt Generator",
            goal="Generate highly effective, contextually optimized prompts",
            backstory="""You are an expert prompt engineer who can analyze user requests 
            and craft the most effective prompts using state-of-the-art frameworks. 
            You understand the nuances of different prompt engineering techniques and 
            can select the best approach for any given request.""",
            allow_delegation=True,
            verbose=True,
            llm="openrouter/anthropic/claude-3-haiku:free",
            tools=[tool]
        )
    
    def generate_optimized_prompt(self, user_input: str, research_output: str = "") -> str:
        """
        Tool function to generate an optimized prompt.
        
        Args:
            user_input: The user's prompt request
            research_output: Research data from the researcher agent
            
        Returns:
            str: The generated optimized prompt
        """
        logger.info(f"Generating optimized prompt for: {user_input[:50]}...")
        
        # If we have research output, extract useful information
        research_data = ""
        if research_output:
            research_data = research_output
        
        # Select the best framework
        framework_name = self._select_best_framework(user_input, research_data)
        logger.info(f"Selected framework: {framework_name}")
        
        # Generate prompt using the selected framework
        generated_prompt = self._generate_prompt_with_framework(framework_name, user_input, research_data)
        
        # Add metadata
        metadata = f"\n\n---\nGenerated using {framework_name} framework\nTimestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        final_prompt = generated_prompt + metadata
        
        return final_prompt