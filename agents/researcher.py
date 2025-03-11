"""
Researcher Agent for NeuroPrompt.
Researches the latest prompt engineering techniques and frameworks.
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

class ResearchTool(BaseTool):
    """Tool for researching prompt engineering techniques."""
    
    name: str = "research_prompt_engineering"
    description: str = "Researches the latest prompt engineering techniques and frameworks"
    agent: Any = Field(description="The ResearcherAgent instance")
    
    def _run(self, query: str) -> str:
        """
        Execute the research.
        
        Args:
            query: The research query
            
        Returns:
            str: The research findings
        """
        return self.agent.research_prompt_engineering(query)

class ResearcherAgent:
    """
    Agent responsible for researching the latest prompt engineering techniques.
    """
    
    def __init__(self, model: str):
        """
        Initialize the Researcher Agent.
        
        Args:
            model: The model ID to use for this agent
        """
        self.model = model
        self._ensure_directories()
        logger.info(f"ResearcherAgent initialized with model: {model}")
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        directories = [
            "documents",
            "documents/frameworks",
            "documents/latest_trends",
            "logs",
            "data"
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def _check_existing_research(self) -> Dict[str, Any]:
        """
        Check for existing research files and their timestamps.
        
        Returns:
            Dict[str, Any]: Information about existing research
        """
        research_info = {
            "has_latest_trends": False,
            "latest_trends_age_days": float('inf'),
            "frameworks": [],
            "framework_info": {}
        }
        
        # Check latest trends file
        latest_trends_path = "documents/latest_trends.md"
        if os.path.exists(latest_trends_path):
            research_info["has_latest_trends"] = True
            
            # Calculate file age in days
            file_timestamp = os.path.getmtime(latest_trends_path)
            file_datetime = datetime.fromtimestamp(file_timestamp)
            age_days = (datetime.now() - file_datetime).days
            research_info["latest_trends_age_days"] = age_days
            
        # Check frameworks
        framework_files = [f for f in os.listdir("documents/frameworks") 
                          if f.endswith(".md")]
        
        research_info["frameworks"] = [f.replace(".md", "") for f in framework_files]
        
        # Get framework info
        for framework in framework_files:
            framework_path = f"documents/frameworks/{framework}"
            if os.path.exists(framework_path):
                framework_name = framework.replace(".md", "")
                file_timestamp = os.path.getmtime(framework_path)
                file_datetime = datetime.fromtimestamp(file_timestamp)
                age_days = (datetime.now() - file_datetime).days
                
                research_info["framework_info"][framework_name] = {
                    "age_days": age_days,
                    "path": framework_path
                }
        
        return research_info
    
    def _save_research_findings(self, 
                               findings: Dict[str, Any], 
                               update_framework_files: bool = True) -> None:
        """
        Save research findings to appropriate files.
        
        Args:
            findings: Dictionary of research findings
            update_framework_files: Whether to update framework files
        """
        # Save latest trends
        if "latest_trends" in findings:
            with open("documents/latest_trends.md", "w") as f:
                f.write(f"# Latest Trends in Prompt Engineering\n\n")
                f.write(f"Updated: {datetime.now().strftime('%Y-%m-%d')}\n\n")
                f.write(findings["latest_trends"])
        
        # Save new or updated frameworks
        if update_framework_files and "frameworks" in findings:
            for framework_name, framework_data in findings["frameworks"].items():
                file_path = f"documents/frameworks/{framework_name}.md"
                
                # Check if this is new or a substantive update
                is_new = not os.path.exists(file_path)
                
                with open(file_path, "w") as f:
                    f.write(f"# {framework_name} Framework\n\n")
                    f.write(f"Updated: {datetime.now().strftime('%Y-%m-%d')}\n\n")
                    
                    if "description" in framework_data:
                        f.write(f"## Description\n\n{framework_data['description']}\n\n")
                    
                    if "structure" in framework_data:
                        f.write(f"## Structure\n\n")
                        for item in framework_data["structure"]:
                            f.write(f"- {item}\n")
                        f.write("\n")
                    
                    if "best_for" in framework_data:
                        f.write(f"## Best For\n\n")
                        for item in framework_data["best_for"]:
                            f.write(f"- {item}\n")
                        f.write("\n")
                    
                    if "example" in framework_data:
                        f.write(f"## Example\n\n{framework_data['example']}\n\n")
                
                if is_new:
                    logger.info(f"Added new framework: {framework_name}")
                else:
                    logger.info(f"Updated framework: {framework_name}")
    
    def get_agent(self) -> Agent:
        """
        Create and return the CrewAI agent.
        
        Returns:
            Agent: The configured CrewAI agent
        """
        tool = ResearchTool(agent=self)
        return Agent(
            role="Research Analyst",
            goal="Research and analyze prompt engineering techniques",
            backstory="""You are an expert researcher specializing in prompt engineering 
            and AI. You have extensive experience in analyzing and documenting the latest 
            developments in AI prompting techniques.""",
            allow_delegation=True,
            verbose=True,
            llm="openrouter/anthropic/claude-3-haiku:free",
            tools=[tool]
        )
    
    def research_prompt_engineering(self, query: str) -> str:
        """
        Tool function to research prompt engineering techniques relevant to the user request.
        
        Args:
            query: The user's prompt request
            
        Returns:
            str: Research findings relevant to the request
        """
        logger.info(f"Researching prompt techniques for: {query[:50]}...")
        
        # Check existing research
        research_info = self._check_existing_research()
        
        # For production, you would implement actual research functionality here
        # This might involve API calls to research databases, web searches, etc.
        # For this example, we'll simulate research with hardcoded data
        
        latest_trends = """
## Current Trends in Prompt Engineering

### Compositional Prompting
Breaking complex tasks into smaller sub-tasks that can be chained together for more reliable results.

### Chain-of-Verification (CoVe)
Having the AI verify its own work by generating multiple solutions and cross-checking them.

### Multimodal Prompting
Techniques for effectively prompting models that handle both text and images.

### Prompt Libraries and Templating
Creating reusable prompt components that can be assembled for specific needs.
        """
        
        # Extract potential keywords from user input to simulate targeted research
        keywords = []
        important_words = ["write", "generate", "create", "analyze", "explain", "summarize", 
                          "creative", "technical", "scientific", "code", "business"]
        
        for word in important_words:
            if word in query.lower():
                keywords.append(word)
        
        # Generate simulated research findings
        content_types = {
            "write": "writing tasks",
            "generate": "content generation",
            "create": "creative work",
            "analyze": "analytical tasks",
            "explain": "explanatory content",
            "summarize": "summarization tasks",
            "creative": "creative content",
            "technical": "technical documentation",
            "scientific": "scientific content",
            "code": "code generation",
            "business": "business content"
        }
        
        # Select relevant frameworks based on keywords
        relevant_frameworks = {}
        
        # This would be based on actual research in a production system
        # For now, we'll use mapped relationships
        framework_relevance = {
            "writing tasks": ["PECRA", "RISEN"],
            "content generation": ["PECRA", "RTF"],
            "creative work": ["RTF", "PECRA"],
            "analytical tasks": ["ReAct", "SCQA"],
            "explanatory content": ["RISEN", "PECRA"],
            "summarization tasks": ["SCQA", "ReAct"],
            "creative content": ["RTF", "PECRA"],
            "technical documentation": ["RISEN", "SCQA"],
            "scientific content": ["ReAct", "SCQA"],
            "code generation": ["ReAct", "RISEN"],
            "business content": ["SCQA", "PECRA"]
        }
        
        # Build list of relevant content types
        relevant_content_types = []
        for keyword in keywords:
            if keyword in content_types:
                relevant_content_types.append(content_types[keyword])
        
        # If we didn't find any specific content types, add a default one
        if not relevant_content_types:
            relevant_content_types = ["general purpose prompts"]
            
        # Select relevant frameworks
        for content_type in relevant_content_types:
            for framework in framework_relevance.get(content_type, ["PECRA"]):
                relevant_frameworks[framework] = True
        
        # If no specific frameworks were selected, add defaults
        if not relevant_frameworks:
            relevant_frameworks = {"PECRA": True, "SCQA": True}
            
        # Prepare research output
        specific_findings = f"## Research Findings for: {query[:100]}...\n\n"
        specific_findings += "### Recommended Prompt Engineering Techniques\n\n"
        
        # Add all relevant techniques
        for framework in relevant_frameworks:
            if framework == "PECRA":
                specific_findings += "- **PECRA Framework** - Ideal for structured prompts with clear role definition and specific request handling.\n"
            elif framework == "SCQA":
                specific_findings += "- **SCQA Framework** - Effective for problem-solving scenarios with clear situation context.\n"
            elif framework == "ReAct":
                specific_findings += "- **ReAct Framework** - Best for complex reasoning tasks requiring step-by-step thinking.\n"
            elif framework == "RTF":
                specific_findings += "- **RTF Framework** - Useful for iterative prompt refinement with feedback loops.\n"
            elif framework == "RISEN":
                specific_findings += "- **RISEN Framework** - Strong for comprehensive instruction following with examples.\n"
        
        specific_findings += "\n### Best Practices for This Request\n\n"
        
        # Add some general best practices
        specific_findings += "1. Be specific about the desired format and level of detail\n"
        specific_findings += "2. Include clear success criteria\n"
        specific_findings += "3. Provide context about the target audience\n"
        
        # Save the research (simulated)
        findings = {
            "latest_trends": latest_trends,
            "specific_findings": specific_findings
        }
        
        # In a real system, you would save these findings to files
        # self._save_research_findings(findings)
        
        # Return the research results
        research_results = f"""
# Prompt Engineering Research

{latest_trends}

{specific_findings}
        """
        
        return research_results