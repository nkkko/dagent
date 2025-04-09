"""Tests for the A2A integration."""
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent.a2a_integration import A2AIntegration

class TestA2AIntegration(unittest.TestCase):
    """Test cases for the A2A integration."""
    
    @patch('src.agent.a2a_integration.A2AClient')
    @patch('src.agent.a2a_integration.RemoteAgentConnection')
    def setUp(self, MockRemoteAgentConnection, MockA2AClient):
        """Set up test fixtures."""
        # Set up mocks
        self.mock_client = MockA2AClient.return_value
        self.mock_connection = MockRemoteAgentConnection.return_value
        
        # Create A2A integration
        self.a2a = A2AIntegration("http://localhost:8080")
        
        # Set up client mock
        self.mock_client.list_agents.return_value = {
            "agents": [
                {"id": "agent1", "name": "Agent 1", "type": "coder"},
                {"id": "agent2", "name": "Agent 2", "type": "general"}
            ]
        }
    
    def test_connect_to_agent(self):
        """Test connecting to an agent."""
        # Connect to agent
        connection = self.a2a.connect_to_agent("agent1")
        
        # Verify connection was created
        self.assertEqual(connection, self.mock_connection)
        self.assertIn("agent1", self.a2a.connections)
    
    def test_disconnect_from_agent(self):
        """Test disconnecting from an agent."""
        # Connect to agent
        self.a2a.connect_to_agent("agent1")
        
        # Disconnect from agent
        self.a2a.disconnect_from_agent("agent1")
        
        # Verify connection was removed
        self.assertNotIn("agent1", self.a2a.connections)
    
    def test_send_message(self):
        """Test sending a message to an agent."""
        # Set up mock response
        self.mock_connection.send_message.return_value = {
            "status": "success",
            "message": "Message received"
        }
        
        # Connect to agent
        self.a2a.connect_to_agent("agent1")
        
        # Send message
        response = self.a2a.send_message(
            agent_id="agent1",
            message="Hello, agent!",
            task_id="task1"
        )
        
        # Verify message was sent
        self.mock_connection.send_message.assert_called_once_with("Hello, agent!", "task1")
        self.assertEqual(response["status"], "success")
    
    def test_list_available_agents(self):
        """Test listing available agents."""
        # List agents
        agents = self.a2a.list_available_agents()
        
        # Verify agents were listed
        self.mock_client.list_agents.assert_called_once()
        self.assertEqual(agents, {"agents": [
            {"id": "agent1", "name": "Agent 1", "type": "coder"},
            {"id": "agent2", "name": "Agent 2", "type": "general"}
        ]})

if __name__ == "__main__":
    unittest.main()