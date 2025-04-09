"""A2A Integration for Daytona Sandbox Orchestration Agent."""
from typing import Any, Dict, Optional

# Import A2A client from samples
import sys
import os
sys.path.append(os.path.abspath("/Users/nikola/dev/dagent/A2A/samples/python"))
from common.client.client import A2AClient
from hosts.multiagent.remote_agent_connection import RemoteAgentConnection

class A2AIntegration:
    """Handles A2A protocol integration for the Daytona agent."""
    
    def __init__(self, host_url: str):
        """Initialize the A2A integration.
        
        Args:
            host_url: The URL of the A2A host.
        """
        self.client = A2AClient(host_url)
        self.connections = {}
        
    def connect_to_agent(self, agent_id: str) -> RemoteAgentConnection:
        """Establish connection to another agent.
        
        Args:
            agent_id: The ID of the agent to connect to.
            
        Returns:
            The established connection.
        """
        connection = RemoteAgentConnection(agent_id, self.client)
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
            # TODO: Implement task creation with A2A client
            task_id = "task-" + str(hash(message))[:8]
            
        # Send message using A2A connection
        response = connection.send_message(message, task_id)
        return response
    
    def list_available_agents(self) -> Dict[str, Any]:
        """List all available agents on the A2A network.
        
        Returns:
            Dictionary of agent information.
        """
        # TODO: Implement agent discovery with A2A client
        return self.client.list_agents()