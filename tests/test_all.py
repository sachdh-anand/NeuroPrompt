#!/usr/bin/env python3
"""
Run all NeuroPrompt tests.
"""
import os
import sys
import unittest
import importlib
import logging
from typing import List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/test_all.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("test_all")

def discover_tests() -> List[str]:
    """
    Discover all test modules in the tests directory.
    
    Returns:
        List[str]: List of test module names
    """
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    test_files = [f for f in os.listdir(tests_dir) 
                 if f.startswith("test_") and f.endswith(".py") and f != "test_all.py"]
    
    return [os.path.splitext(f)[0] for f in test_files]

def run_test_module(module_name: str) -> Tuple[bool, str]:
    """
    Run tests in a specific module.
    
    Args:
        module_name: Name of the test module
        
    Returns:
        Tuple[bool, str]: Success status and result message
    """
    try:
        # Import the module
        module = importlib.import_module(f"tests.{module_name}")
        
        # Create a test suite and run tests
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(module)
        
        # Run tests with a test result collector
        result = unittest.TextTestResult(sys.stdout, descriptions=True, verbosity=2)
        suite.run(result)
        
        # Check results
        if result.wasSuccessful():
            return True, f"All tests in {module_name} passed"
        else:
            failures = len(result.failures)
            errors = len(result.errors)
            return False, f"{module_name} had {failures} failures and {errors} errors"
            
    except Exception as e:
        return False, f"Error running {module_name}: {str(e)}"

def main() -> int:
    """
    Run all tests and report results.
    
    Returns:
        int: Exit code (0 for success, 1 for failures)
    """
    print("=" * 70)
    print("Running all NeuroPrompt tests")
    print("=" * 70)
    
    # Create necessary directories
    os.makedirs("logs", exist_ok=True)
    
    # Discover test modules
    test_modules = discover_tests()
    
    if not test_modules:
        print("No test modules found!")
        return 1
    
    print(f"Found {len(test_modules)} test modules: {', '.join(test_modules)}")
    print("-" * 70)
    
    # Run each test module
    results = []
    for module in test_modules:
        print(f"\nRunning tests in {module}...")
        success, message = run_test_module(module)
        results.append((module, success, message))
        print(f"Result: {'✅ PASS' if success else '❌ FAIL'} - {message}")
    
    # Print summary
    print("\n" + "=" * 70)
    print("Test Summary:")
    print("-" * 70)
    
    passed = sum(1 for _, success, _ in results if success)
    failed = len(results) - passed
    
    for module, success, message in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {module}")
    
    print("-" * 70)
    print(f"Total: {len(results)} test modules, {passed} passed, {failed} failed")
    print("=" * 70)
    
    # Return appropriate exit code
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())