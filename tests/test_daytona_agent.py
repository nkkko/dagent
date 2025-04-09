"""Tests for the Daytona Sandbox Orchestration Agent."""
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent.daytona_agent import DaytonaSandboxAgent

class TestDaytonaSandboxAgent(unittest.TestCase):
    """Test cases for the Daytona Sandbox Orchestration Agent."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock LLM
        self.mock_llm = MagicMock()
        
        # Create agent with mock LLM
        self.agent = DaytonaSandboxAgent(
            name="test-agent",
            model=self.mock_llm
        )
    
    def test_create_sandbox(self):
        """Test creating a sandbox."""
        # Create sandbox
        sandbox = self.agent.create_sandbox(
            name="test-sandbox",
            template="python-dev"
        )
        
        # Verify sandbox was created
        self.assertEqual(sandbox["name"], "test-sandbox")
        self.assertEqual(sandbox["template"], "python-dev")
        self.assertEqual(sandbox["status"], "creating")
        self.assertIn("id", sandbox)
        self.assertIn("url", sandbox)
    
    def test_configure_sandbox(self):
        """Test configuring a sandbox."""
        # Create sandbox
        sandbox = self.agent.create_sandbox(
            name="test-sandbox",
            template="python-dev"
        )
        
        # Get sandbox ID
        sandbox_id = sandbox["id"]
        
        # Configure sandbox
        configuration = {"memory": "4Gi"}
        updated_sandbox = self.agent.configure_sandbox(
            sandbox_id=sandbox_id,
            configuration=configuration
        )
        
        # Verify sandbox was configured
        self.assertEqual(updated_sandbox["status"], "configured")
    
    def test_delete_sandbox(self):
        """Test deleting a sandbox."""
        # Create sandbox
        sandbox = self.agent.create_sandbox(
            name="test-sandbox",
            template="python-dev"
        )
        
        # Get sandbox ID
        sandbox_id = sandbox["id"]
        
        # Delete sandbox
        result = self.agent.delete_sandbox(sandbox_id)
        
        # Verify sandbox was deleted
        self.assertEqual(result["status"], "success")
        
        # Verify sandbox is no longer in the list
        with self.assertRaises(ValueError):
            self.agent.delete_sandbox(sandbox_id)
    
    def test_list_sandboxes(self):
        """Test listing sandboxes."""
        # Initially, there should be no sandboxes
        sandboxes = self.agent.list_sandboxes()
        self.assertEqual(len(sandboxes), 0)
        
        # Create some sandboxes
        self.agent.create_sandbox(name="sandbox1", template="python-dev")
        self.agent.create_sandbox(name="sandbox2", template="node-dev")
        
        # List sandboxes
        sandboxes = self.agent.list_sandboxes()
        
        # Verify sandboxes are listed
        self.assertEqual(len(sandboxes), 2)
        self.assertEqual(sandboxes[0]["name"], "sandbox1")
        self.assertEqual(sandboxes[1]["name"], "sandbox2")

if __name__ == "__main__":
    unittest.main()