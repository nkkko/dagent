"""Main application for Daytona Sandbox Orchestration Agent."""
import argparse
import logging
import os
import dotenv
from typing import Any, Dict, Optional

from google.adk.models import GoogleLLM
from google.adk.tools import FunctionTool
from agent.daytona_agent import DaytonaSandboxAgent
from agent.a2a_integration import A2AIntegration
from agent.tools import DaytonaToolset

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
        llm = GoogleLLM(api_key=args.gemini_key)
        logger.info("Using Gemini LLM with provided API key")
    else:
        llm = GoogleLLM()
        logger.info("Using Gemini LLM with default configuration")
    
    # Log configuration
    logger.info(f"Using Daytona API URL: {args.api_url}")
    logger.info(f"Using Daytona API Target: {args.api_target}")
    logger.info(f"Using A2A Host URL: {args.host_url}")
    
    # Create agent
    agent = DaytonaSandboxAgent(
        name="daytona-sandbox-agent",
        model=llm,
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
    
    # Create and register Daytona toolset
    daytona_toolset = DaytonaToolset(args.api_url, args.api_key)
    for tool in daytona_toolset.as_tools():
        agent.register_tool(tool)
    
    # Set up A2A integration
    a2a = A2AIntegration(args.host_url)
    agent.a2a = a2a
    
    # Add A2A communication tools
    agent.register_tool(FunctionTool(agent.connect_to_coder_agent))
    agent.register_tool(FunctionTool(agent.send_message_to_agent))
    agent.register_tool(FunctionTool(agent.list_available_agents))
    
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
        
        # For demonstration, add some agent methods
        DaytonaSandboxAgent.connect_to_coder_agent = connect_to_coder_agent
        DaytonaSandboxAgent.send_message_to_agent = send_message_to_agent
        DaytonaSandboxAgent.list_available_agents = list_available_agents
        
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

def connect_to_coder_agent(self, coder_agent_id: str) -> Dict[str, Any]:
    """Connect to the coder agent.
    
    Args:
        coder_agent_id: ID of the coder agent to connect to.
        
    Returns:
        Connection status.
    """
    connection = self.a2a.connect_to_agent(coder_agent_id)
    return {
        "status": "connected",
        "agent_id": coder_agent_id,
        "connection_id": id(connection)
    }

def send_message_to_agent(
    self, 
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
    return self.a2a.send_message(agent_id, message, task_id)

def list_available_agents(self) -> Dict[str, Any]:
    """List all available agents.
    
    Returns:
        Available agents information.
    """
    return self.a2a.list_available_agents()

if __name__ == "__main__":
    main()