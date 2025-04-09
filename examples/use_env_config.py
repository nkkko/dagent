"""Example demonstrating how to use environment variables with the Daytona agent."""
import os
import sys
import logging
import dotenv
from typing import Dict, Any

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent.daytona_agent import DaytonaSandboxAgent
from src.agent.tools import DaytonaToolset
from google.adk.models import GoogleLLM

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_environment() -> Dict[str, str]:
    """Load environment variables from .env file.
    
    Returns:
        Dictionary of environment variables.
    """
    # Load .env file if it exists
    dotenv.load_dotenv()
    
    # Get required environment variables
    env_vars = {
        "DAYTONA_API_KEY": os.getenv("DAYTONA_API_KEY"),
        "DAYTONA_API_URL": os.getenv("DAYTONA_API_URL"),
        "DAYTONA_API_TARGET": os.getenv("DAYTONA_API_TARGET"),
        "A2A_HOST_URL": os.getenv("A2A_HOST_URL"),
    }
    
    # Check for missing environment variables
    missing_vars = [k for k, v in env_vars.items() if v is None]
    if missing_vars:
        logger.warning(f"Missing environment variables: {', '.join(missing_vars)}")
    
    return env_vars

def create_agent_with_env_config() -> DaytonaSandboxAgent:
    """Create a Daytona agent with configuration from environment variables.
    
    Returns:
        Configured Daytona agent.
    """
    # Load environment variables
    env = load_environment()
    
    # Log configuration
    logger.info(f"Daytona API URL: {env.get('DAYTONA_API_URL')}")
    logger.info(f"Daytona API Target: {env.get('DAYTONA_API_TARGET')}")
    logger.info(f"A2A Host URL: {env.get('A2A_HOST_URL')}")
    
    # Create LLM
    llm = GoogleLLM()
    
    # Create agent
    agent = DaytonaSandboxAgent(
        name="daytona-sandbox-agent",
        model=llm,
        description=f"Daytona sandbox agent for target: {env.get('DAYTONA_API_TARGET', 'unknown')}"
    )
    
    # Create Daytona toolset with API configuration
    daytona_toolset = DaytonaToolset(
        api_url=env.get('DAYTONA_API_URL', 'http://localhost:8090'),
        api_key=env.get('DAYTONA_API_KEY')
    )
    
    # Register tools
    for tool in daytona_toolset.as_tools():
        agent.register_tool(tool)
    
    return agent

def main() -> None:
    """Main entry point for the example."""
    try:
        # Create agent with environment configuration
        agent = create_agent_with_env_config()
        logger.info("Agent created successfully")
        
        # List available sandboxes (this would use the API key from environment)
        sandboxes = agent.list_sandboxes()
        logger.info(f"Found {len(sandboxes)} sandboxes")
        
        # Create a new sandbox
        sandbox = agent.create_sandbox(
            name="env-example-sandbox",
            template="python-dev",
            resources={"size": "small"}
        )
        logger.info(f"Created sandbox: {sandbox['id']}")
        
        # Clean up
        agent.delete_sandbox(sandbox["id"])
        logger.info(f"Deleted sandbox: {sandbox['id']}")
        
    except Exception as e:
        logger.error(f"Error in example: {e}", exc_info=True)

if __name__ == "__main__":
    main()