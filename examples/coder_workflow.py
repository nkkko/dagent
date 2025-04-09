"""Example workflow between Daytona agent and Coder agent."""
import os
import sys
import logging
import json
from typing import Dict, Any, List

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent.daytona_agent import DaytonaSandboxAgent
from src.agent.a2a_integration import A2AIntegration
from google.adk.models import Gemini

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowSimulator:
    """Simulates a workflow between Daytona agent and Coder agent."""
    
    def __init__(self):
        """Initialize the workflow simulator."""
        # Create agents
        self.daytona_agent = self._create_daytona_agent()
        
        # Mock coder agent responses
        self.coder_responses = {
            "request_environment": {
                "type": "create_sandbox",
                "name": "web-app-project",
                "template_id": "node-dev",
                "resource_size": "medium",
                "requirements": [
                    "Node.js 16+",
                    "React",
                    "PostgreSQL"
                ]
            },
            "acknowledge_environment": {
                "type": "acknowledge",
                "message": "Thank you, I'll start working in the environment."
            },
            "request_code_execution": {
                "type": "execute",
                "command": "npm install react react-dom",
                "sandbox_id": "{sandbox_id}"
            },
            "complete_task": {
                "type": "complete",
                "sandbox_id": "{sandbox_id}",
                "message": "I've completed the development task. You can clean up the environment."
            }
        }
    
    def _create_daytona_agent(self) -> DaytonaSandboxAgent:
        """Create and configure the Daytona agent.
        
        Returns:
            Configured Daytona agent.
        """
        # Create LLM
        llm = Gemini(model="gemini-2.0-flash")
        
        # Create agent
        agent = DaytonaSandboxAgent(
            name="daytona_agent",
            model=llm
        )
        
        # Set up A2A integration
        a2a = A2AIntegration("http://localhost:8080")
        agent._a2a_client = a2a
        
        # Communication tools are already registered in the agent
        
        return agent
    
    def simulate_workflow(self):
        """Simulate a workflow between Daytona agent and Coder agent."""
        logger.info("Starting workflow simulation")
        
        # Step 1: Coder agent requests environment
        logger.info("Step 1: Coder agent requests environment")
        coder_request = self.coder_responses["request_environment"]
        
        # Daytona agent creates sandbox
        sandbox = self.daytona_agent.create_sandbox(
            name=coder_request["name"],
            template=coder_request["template_id"],
            resources={"size": coder_request["resource_size"]}
        )
        
        logger.info(f"Created sandbox: {json.dumps(sandbox, indent=2)}")
        
        # Step 2: Daytona agent notifies coder agent
        logger.info("Step 2: Daytona agent notifies coder agent")
        notification = {
            "type": "environment_ready",
            "sandbox_id": sandbox["id"],
            "url": sandbox["url"],
            "credentials": {
                "username": "developer",
                "password": "example-password"
            }
        }
        
        logger.info(f"Notification to coder agent: {json.dumps(notification, indent=2)}")
        
        # Step 3: Coder agent acknowledges
        logger.info("Step 3: Coder agent acknowledges")
        acknowledge = self.coder_responses["acknowledge_environment"]
        logger.info(f"Acknowledgment from coder agent: {json.dumps(acknowledge, indent=2)}")
        
        # Step 4: Coder agent requests code execution
        logger.info("Step 4: Coder agent requests code execution")
        execution_request = self.coder_responses["request_code_execution"]
        execution_request["sandbox_id"] = sandbox["id"]
        
        logger.info(f"Execution request from coder agent: {json.dumps(execution_request, indent=2)}")
        
        # Daytona agent simulates execution
        execution_result = {
            "status": "success",
            "output": "added 2 packages, and audited 1285 packages in 3s\n\n228 packages are looking for funding\n  run `npm fund` for details\n\nfound 0 vulnerabilities",
            "sandbox_id": sandbox["id"]
        }
        
        logger.info(f"Execution result: {json.dumps(execution_result, indent=2)}")
        
        # Step 5: Coder agent completes task
        logger.info("Step 5: Coder agent completes task")
        completion = self.coder_responses["complete_task"]
        completion["sandbox_id"] = sandbox["id"]
        
        logger.info(f"Completion from coder agent: {json.dumps(completion, indent=2)}")
        
        # Step 6: Daytona agent deletes sandbox
        logger.info("Step 6: Daytona agent deletes sandbox")
        deletion_result = self.daytona_agent.delete_sandbox(sandbox["id"])
        
        logger.info(f"Deletion result: {json.dumps(deletion_result, indent=2)}")
        
        logger.info("Workflow simulation completed")

def main():
    """Run the workflow simulation."""
    simulator = WorkflowSimulator()
    simulator.simulate_workflow()

if __name__ == "__main__":
    main()