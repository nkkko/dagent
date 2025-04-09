"""A2A Integration for Daytona Sandbox Orchestration Agent."""
from typing import Any, Dict, Optional, List
import os
import sys

# Add A2A samples to path
A2A_SAMPLES_PATH = os.path.abspath(os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "A2A", "samples", "python"
))
sys.path.append(A2A_SAMPLES_PATH)

# Import A2A client from samples
try:
    from common.client.client import A2AClient
    from hosts.multiagent.remote_agent_connection import RemoteAgentConnections
    
    # Use the actual RemoteAgentConnections class
    print("Successfully imported A2A clients")
    USE_REAL_A2A = True
except ImportError as e:
    print(f"Warning: Could not import A2A client: {e}")
    print(f"Using path: {A2A_SAMPLES_PATH}")
    print(f"Contents: {os.listdir(A2A_SAMPLES_PATH) if os.path.exists(A2A_SAMPLES_PATH) else 'Path does not exist'}")
    
    # Fallback to mock implementation
    USE_REAL_A2A = False
    
    class A2AClient:
        """Mock A2A client for demonstration purposes."""
        
        def __init__(self, url: str):
            """Initialize the A2A client.
            
            Args:
                url: The URL of the A2A host.
            """
            self.url = url
        
        def list_agents(self) -> Dict[str, Any]:
            """List available agents.
            
            Returns:
                Dictionary of agent information.
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
    
    # We need to create our own mock for RemoteAgentConnections
    class RemoteAgentConnections:
        """Connection to a remote agent."""
        
        def __init__(self, agent_id: str, client: A2AClient):
            """Initialize a remote agent connection.
            
            Args:
                agent_id: The ID of the agent to connect to.
                client: The A2A client to use for communication.
            """
            self.agent_id = agent_id
            self.client = client
        
        def send_message(self, message: str, task_id: str) -> Dict[str, Any]:
            """Send a message to the remote agent.
            
            Args:
                message: The message to send.
                task_id: The task ID to associate with the message.
                
            Returns:
                The response from the agent.
            """
            # Mock implementation
            return {
                "status": "success",
                "task_id": task_id,
                "agent_id": self.agent_id,
                "response": f"Received message: {message[:50]}...",
                "timestamp": "2023-04-09T12:00:00Z"
            }

class A2AIntegration:
    """Handles A2A protocol integration for the Daytona agent."""
    
    def __init__(self, host_url: str):
        """Initialize the A2A integration.
        
        Args:
            host_url: The URL of the A2A host.
        """
        self.client = A2AClient(host_url)
        self.connections = {}
        
    def connect_to_agent(self, agent_id: str) -> RemoteAgentConnections:
        """Establish connection to another agent.
        
        Args:
            agent_id: The ID of the agent to connect to.
            
        Returns:
            The established connection.
        """
        if USE_REAL_A2A:
            # TODO: This is a placeholder. We need a proper implementation
            # that converts agent_id to AgentCard for RemoteAgentConnections
            from common.types import AgentCard, AgentProvider, AgentCapabilities, AgentAuthentication, AgentSkill
            
            # Create a mock AgentCard based on agent_id
            agent_card = AgentCard(
                name=f"Agent {agent_id}",
                url=f"http://localhost:8080/agents/{agent_id}",
                version="1.0.0",
                provider=AgentProvider(organization="Example Org"),
                capabilities=AgentCapabilities(streaming=False),
                authentication=AgentAuthentication(schemes=["none"]),
                skills=[AgentSkill(id="skill1", name="Skill 1")]
            )
            
            # Create a real RemoteAgentConnections instance
            connection = RemoteAgentConnections(agent_card)
        else:
            # Use our mock implementation
            connection = RemoteAgentConnections(agent_id, self.client)
            
        self.connections[agent_id] = connection
        return connection
        
    def disconnect_from_agent(self, agent_id: str) -> None:
        """Disconnect from an agent.
        
        Args:
            agent_id: The ID of the agent to disconnect from.
        """
        if agent_id in self.connections:
            # Close connection if needed
            del self.connections[agent_id]
    
    def send_message(self, 
                    agent_id: str, 
                    message: str, 
                    task_id: Optional[str] = None) -> Dict[str, Any]:
        """Send a message to another agent.
        
        Args:
            agent_id: The ID of the agent to send the message to.
            message: The message content.
            task_id: Optional task ID to associate with this message.
            
        Returns:
            Response from the agent.
        """
        if agent_id not in self.connections:
            connection = self.connect_to_agent(agent_id)
        else:
            connection = self.connections[agent_id]
            
        # Create task if task_id not provided
        if not task_id:
            task_id = "task-" + str(hash(message))[:8]
            
        # Send message using A2A connection
        response = connection.send_message(message, task_id)
        return response
    
    def list_available_agents(self) -> Dict[str, Any]:
        """List all available agents on the A2A network.
        
        Returns:
            Dictionary of agent information.
        """
        return self.client.list_agents()