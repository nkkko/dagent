#!/usr/bin/env python
"""Test A2A import."""
import os
import sys

# Add A2A samples to path
A2A_SAMPLES_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    "A2A", "samples", "python"
))
sys.path.append(A2A_SAMPLES_PATH)

# Try to import A2A client
try:
    from common.client.client import A2AClient
    print("A2AClient imported successfully")
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Using path: {A2A_SAMPLES_PATH}")
    print(f"Contents: {os.listdir(A2A_SAMPLES_PATH) if os.path.exists(A2A_SAMPLES_PATH) else 'Path does not exist'}")

# Try to import RemoteAgentConnection
try:
    from hosts.multiagent.remote_agent_connection import RemoteAgentConnection
    print("RemoteAgentConnection imported successfully")
except ImportError as e:
    print(f"RemoteAgentConnection import error: {e}")
    
    # List contents of the hosts directory
    hosts_path = os.path.join(A2A_SAMPLES_PATH, "hosts")
    multiagent_path = os.path.join(hosts_path, "multiagent")
    
    print(f"Hosts path: {hosts_path}")
    print(f"Hosts contents: {os.listdir(hosts_path) if os.path.exists(hosts_path) else 'Path does not exist'}")
    
    print(f"Multiagent path: {multiagent_path}")
    print(f"Multiagent contents: {os.listdir(multiagent_path) if os.path.exists(multiagent_path) else 'Path does not exist'}")
    
    print(f"Python path: {sys.path}")