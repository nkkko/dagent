"""Example demonstrating communication between Daytona agent and Coder agent."""
import os
import sys
import logging
from typing import Dict, Any

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent.daytona_agent import DaytonaSandboxAgent
from src.agent.a2a_integration import A2AIntegration
from src.config import get_template_by_id, get_resource_config
from google.adk.models import Gemini
from google.adk.tools import FunctionTool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_agent() -> DaytonaSandboxAgent:
    """Create and configure the Daytona agent.
    
    Returns:
        Configured agent.
    """
    # Create LLM
    llm = Gemini(model="gemini-2.0-flash")
    
    # Create agent
    agent = DaytonaSandboxAgent(
        name="daytona_sandbox_agent",
        model=llm,
        description="An agent that orchestrates Daytona sandbox environments",
    )
    
    # Set up A2A integration
    a2a = A2AIntegration("http://localhost:8080")
    agent.a2a = a2a
    
    # Add communication methods
    agent.connect_to_coder_agent = connect_to_coder_agent.__get__(agent)
    agent.send_message_to_coder = send_message_to_coder.__get__(agent)
    agent.handle_coder_request = handle_coder_request.__get__(agent)
    
    # Register tools
    agent.register_tool(FunctionTool(agent.connect_to_coder_agent))
    agent.register_tool(FunctionTool(agent.send_message_to_coder))
    agent.register_tool(FunctionTool(agent.handle_coder_request))
    
    return agent

def connect_to_coder_agent(self, coder_agent_id: str) -> Dict[str, Any]:
    """Connect to the coder agent.
    
    Args:
        coder_agent_id: The ID of the coder agent.
        
    Returns:
        Connection status.
    """
    logger.info(f"Connecting to coder agent: {coder_agent_id}")
    connection = self.a2a.connect_to_agent(coder_agent_id)
    
    return {
        "status": "connected",
        "agent_id": coder_agent_id,
        "connection_id": id(connection)
    }

def send_message_to_coder(self, coder_agent_id: str, message: str) -> Dict[str, Any]:
    """Send a message to the coder agent.
    
    Args:
        coder_agent_id: The ID of the coder agent.
        message: The message to send.
        
    Returns:
        Response from the coder agent.
    """
    logger.info(f"Sending message to coder agent {coder_agent_id}: {message}")
    response = self.a2a.send_message(coder_agent_id, message)
    logger.info(f"Response from coder agent: {response}")
    
    return response

def handle_coder_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
    """Handle a request from the coder agent.
    
    Args:
        request: The request from the coder agent.
        
    Returns:
        Response to the coder agent.
    """
    logger.info(f"Handling request from coder agent: {request}")
    
    request_type = request.get("type")
    
    if request_type == "create_sandbox":
        # Extract request details
        template_id = request.get("template_id", "python-dev")
        resource_size = request.get("resource_size", "small")
        
        # Get template and resource config
        try:
            template = get_template_by_id(template_id)
            resources = get_resource_config(resource_size)
            
            # Create sandbox
            sandbox = self.create_sandbox(
                name=request.get("name", f"sandbox-{template_id}"),
                template=template_id,
                resources=resources
            )
            
            return {
                "status": "success",
                "sandbox": sandbox,
                "message": f"Created sandbox {sandbox['id']} with {template_id} template"
            }
        except ValueError as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    elif request_type == "delete_sandbox":
        sandbox_id = request.get("sandbox_id")
        
        if not sandbox_id:
            return {
                "status": "error",
                "error": "sandbox_id is required"
            }
        
        try:
            result = self.delete_sandbox(sandbox_id)
            return {
                "status": "success",
                "message": f"Deleted sandbox {sandbox_id}"
            }
        except ValueError as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    else:
        return {
            "status": "error",
            "error": f"Unknown request type: {request_type}"
        }

def main() -> None:
    """Main entry point for the example."""
    try:
        # Create agent
        agent = create_agent()
        logger.info("Daytona agent created and initialized")
        
        # Connect to coder agent (example)
        coder_agent_id = "coder-agent-1"
        connection = agent.connect_to_coder_agent(coder_agent_id)
        logger.info(f"Connection established: {connection}")
        
        # Simulate receiving a request from the coder agent
        example_request = {
            "type": "create_sandbox",
            "name": "django-project",
            "template_id": "python-dev",
            "resource_size": "medium"
        }
        
        # Handle the request
        response = agent.handle_coder_request(example_request)
        logger.info(f"Response to coder request: {response}")
        
        # Send a message to the coder agent
        if response["status"] == "success":
            message = f"Your sandbox {response['sandbox']['id']} is ready at {response['sandbox']['url']}"
            agent.send_message_to_coder(coder_agent_id, message)
        
        logger.info("Example completed")
        
    except Exception as e:
        logger.error(f"Error in example: {e}", exc_info=True)

if __name__ == "__main__":
    main()