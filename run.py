#!/usr/bin/env python3
"""
NeuroPrompt - Main Entry Point
The world's best open-source AI prompt generator using CrewAI.
"""
import os
import sys
import argparse
from typing import Dict, Any
from dotenv import load_dotenv
from core.logger import get_logger, restore_stdout_stderr

# Ensure necessary directories exist
os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True)
os.makedirs("documents/frameworks", exist_ok=True)

# Get logger instance
logger = get_logger("neuroprompt")

# Load environment variables
load_dotenv()

# Import NeuroPromptCrew
from core.crew import NeuroPromptCrew


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="NeuroPrompt - The world's best AI prompt generator"
    )
    
    parser.add_argument(
        "input",
        type=str,
        nargs="?",
        help="The prompt request to process"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Output file to save the generated prompt (optional)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser.parse_args()


def run_neuroprompt(user_input: str, verbose: bool = False) -> Dict[str, Any]:
    """
    Run the NeuroPrompt system with the given input.
    
    Args:
        user_input: User's prompt request
        verbose: Whether to enable verbose output
        
    Returns:
        Dict containing the results
    """
    try:
        logger.info(f"Starting NeuroPrompt with input: {user_input}")
        
        # Initialize NeuroPromptCrew
        crew = NeuroPromptCrew()
        
        # Run the crew process
        results = crew.generate_prompt(user_input)
        
        return results
    except Exception as e:
        logger.error(f"Error in NeuroPrompt: {str(e)}")
        raise


def main() -> None:
    """Main entry point for the application."""
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Get user input from arguments or prompt
        if args.input:
            user_input = args.input
        else:
            user_input = input("Enter your prompt request: ")
        
        # Run NeuroPrompt
        results = run_neuroprompt(user_input, args.verbose)
        
        # Print final prompt
        print("\n==================================================")
        print("GENERATED PROMPT:")
        print("==================================================")
        print(results["final_prompt"])
        print("==================================================\n")
        
        # Save to file if specified
        if args.output:
            try:
                with open(args.output, "w") as f:
                    f.write(results["final_prompt"])
                logger.info(f"Prompt saved to {args.output}")
                print(f"Prompt saved to {args.output}")
            except Exception as e:
                logger.error(f"Error saving prompt to file: {str(e)}")
                print(f"Error saving prompt to file: {str(e)}")
    finally:
        # Restore stdout/stderr at the end to prevent issues on exit
        restore_stdout_stderr()


if __name__ == "__main__":
    main()