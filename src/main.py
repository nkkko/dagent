"""Main application for Daytona Sandbox Orchestration Agent."""
import argparse
import logging
import os
import dotenv
from typing import Any, Dict, Optional

from google.adk.models import Gemini
from google.adk.tools import FunctionTool
from agent.daytona_agent import DaytonaSandboxAgent
from agent.a2a_integration import A2AIntegration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
dotenv.load_dotenv()

def parse_args() -> argparse.Namespace:
    """Parse command line arguments.
    
    Returns:
        Parsed arguments.
    """
    # Get default values from environment variables
    default_host_url = os.getenv("A2A_HOST_URL", "http://localhost:8080")
    default_api_url = os.getenv("DAYTONA_API_URL", "http://localhost:8090")
    default_api_key = os.getenv("DAYTONA_API_KEY")
    default_api_target = os.getenv("DAYTONA_API_TARGET", "us")
    default_gemini_key = os.getenv("GEMINI_API_KEY")
    
    parser = argparse.ArgumentParser(description="Daytona Sandbox Orchestration Agent")
    parser.add_argument(
        "--host-url", 
        default=default_host_url,
        help=f"URL for the A2A host server (default: {default_host_url})"
    )
    parser.add_argument(
        "--api-url", 
        default=default_api_url,
        help=f"URL for the Daytona API (default: {default_api_url})"
    )
    parser.add_argument(
        "--api-key", 
        default=default_api_key,
        help="API key for Daytona API authentication"
    )
    parser.add_argument(
        "--api-target", 
        default=default_api_target,
        help=f"Daytona API target region (default: {default_api_target})"
    )
    parser.add_argument(
        "--gemini-key",
        default=default_gemini_key,
        help="API key for Gemini LLM"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose logging"
    )
    return parser.parse_args()

def create_agent(args: argparse.Namespace) -> DaytonaSandboxAgent:
    """Create and configure the agent.
    
    Args:
        args: Command line arguments.
        
    Returns:
        Configured agent.
    """
    # Create LLM with API key if available
    if args.gemini_key:
        llm = Gemini(model="gemini-2.0-flash")  # API key is handled through environment variables
        logger.info("Using Gemini LLM with provided API key")
    else:
        llm = Gemini(model="gemini-2.0-flash")
        logger.info("Using Gemini LLM with default configuration")
    
    # Log configuration
    logger.info(f"Using Daytona API URL: {args.api_url}")
    logger.info(f"Using Daytona API Target: {args.api_target}")
    logger.info(f"Using A2A Host URL: {args.host_url}")
    
    # Set up A2A integration
    a2a = A2AIntegration(args.host_url)
    
    # Create communication tools
    communication_tools = [
        FunctionTool(connect_to_coder_agent),
        FunctionTool(send_message_to_agent),
        FunctionTool(list_available_agents)
    ]
    
    # Create agent with tools
    agent = DaytonaSandboxAgent(
        name="daytona_sandbox_agent",
        model=llm,
        tools=communication_tools,
        description=f"An agent that orchestrates Daytona sandbox environments ({args.api_target}) and communicates with other agents.",
        instruction="""You are a Daytona sandbox orchestration agent. Your primary responsibilities are:
1. Creating and managing Daytona sandbox environments
2. Communicating with other agents, especially the coder agent, to coordinate development activities
3. Providing status and information about available sandboxes
4. Configuring sandboxes based on development requirements

When communicating with other agents:
- Be clear and concise
- Include all necessary details about sandboxes
- Follow up on requests in a timely manner
- Handle errors gracefully and provide helpful feedback
"""
    )
    
    # Store A2A integration for use by tools
    agent._a2a_client = a2a
    
    return agent

def main() -> None:
    """Main entry point for the application."""
    args = parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        logger.info("Starting Daytona Sandbox Orchestration Agent")
        agent = create_agent(args)
        
        # TODO: Start agent server or interface
        logger.info("Agent initialized and ready to receive requests")
        
        # TODO: Add proper agent lifecycle management
        
    except Exception as e:
        logger.error(f"Error starting agent: {e}", exc_info=True)
        exit(1)
    
    # Keep the application running
    try:
        # This would be replaced with proper server code
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Agent shutting down")

def connect_to_coder_agent(coder_agent_id: str) -> Dict[str, Any]:
    """Connect to the coder agent.
    
    Args:
        coder_agent_id: ID of the coder agent to connect to.
        
    Returns:
        Connection status.
    """
    # This function is used as a tool, it will get 'self' from the agent
    # when registered as a tool
    connection = None
    
    # Mock implementation
    return {
        "status": "connected",
        "agent_id": coder_agent_id,
        "connection_id": 12345
    }

def send_message_to_agent(
    agent_id: str, 
    message: str, 
    task_id: Optional[str] = None
) -> Dict[str, Any]:
    """Send a message to another agent.
    
    Args:
        agent_id: ID of the agent to send the message to.
        message: Message content.
        task_id: Optional task ID.
        
    Returns:
        Response from the agent.
    """
    # Mock implementation
    return {
        "status": "success",
        "agent_id": agent_id,
        "task_id": task_id or "task-12345",
        "response": f"Received message: {message[:50]}...",
        "timestamp": "2023-04-09T12:00:00Z"
    }

def list_available_agents() -> Dict[str, Any]:
    """List all available agents.
    
    Returns:
        Available agents information.
    """
    # Mock implementation
    return {
        "agents": [
            {
                "id": "coder-agent",
                "name": "Coder Agent",
                "type": "development",
                "capabilities": ["code-generation", "code-review"]
            }
        ]
    }

if __name__ == "__main__":
    main()