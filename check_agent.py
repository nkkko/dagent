"""Script to check the LlmAgent class API."""
from google.adk.agents import LlmAgent

print("LlmAgent attributes and methods:")
print(dir(LlmAgent))

# Try to create an instance
print("\nCreating instance:")
try:
    agent = LlmAgent(name="test_agent")
    print("Instance created successfully")
    print("Instance attributes and methods:")
    print(dir(agent))
except Exception as e:
    print(f"Error creating instance: {e}")