"""Configuration for the Daytona Sandbox Orchestration Agent."""
from typing import Dict, Any, List

# Default sandbox templates
DEFAULT_TEMPLATES = [
    {
        "id": "python-dev",
        "name": "Python Development Environment",
        "description": "Environment for Python development with common tools and libraries",
        "base_image": "python:3.9",
        "installed_packages": ["pytest", "black", "isort", "mypy", "flake8"],
        "setup_commands": [
            "pip install -r requirements.txt",
        ],
    },
    {
        "id": "node-dev",
        "name": "Node.js Development Environment",
        "description": "Environment for Node.js development with common tools and libraries",
        "base_image": "node:16",
        "installed_packages": ["typescript", "eslint", "prettier", "jest"],
        "setup_commands": [
            "npm install",
        ],
    },
    {
        "id": "go-dev",
        "name": "Go Development Environment",
        "description": "Environment for Go development with common tools and libraries",
        "base_image": "golang:1.18",
        "installed_packages": [],
        "setup_commands": [
            "go mod download",
        ],
    },
]

# Default resource configurations
DEFAULT_RESOURCE_CONFIGS = {
    "small": {
        "cpu": "1",
        "memory": "2Gi",
        "disk": "10Gi",
    },
    "medium": {
        "cpu": "2",
        "memory": "4Gi",
        "disk": "20Gi",
    },
    "large": {
        "cpu": "4",
        "memory": "8Gi",
        "disk": "40Gi",
    },
}

# Agent configurations
AGENT_CONFIG = {
    "name": "daytona-sandbox-agent",
    "description": "An agent that orchestrates Daytona sandbox environments",
    "version": "0.1.0",
    "supported_agent_interfaces": [
        "coder",  # The coder agent interface
        "general",  # General purpose agent interface
    ],
}

# A2A protocol configurations
A2A_CONFIG = {
    "default_host_url": "http://localhost:8080",
    "default_session_timeout": 3600,  # 1 hour in seconds
    "heartbeat_interval": 30,  # seconds
}

# Daytona API configurations
DAYTONA_API_CONFIG = {
    "default_api_url": "http://localhost:8090",
    "default_timeout": 60,  # seconds
}

def get_template_by_id(template_id: str) -> Dict[str, Any]:
    """Get a template by ID.
    
    Args:
        template_id: The ID of the template.
        
    Returns:
        The template configuration.
        
    Raises:
        ValueError: If the template does not exist.
    """
    for template in DEFAULT_TEMPLATES:
        if template["id"] == template_id:
            return template
    raise ValueError(f"Template with ID '{template_id}' not found")

def get_resource_config(size: str) -> Dict[str, str]:
    """Get a resource configuration by size.
    
    Args:
        size: The size of the resource configuration.
        
    Returns:
        The resource configuration.
        
    Raises:
        ValueError: If the resource configuration does not exist.
    """
    if size not in DEFAULT_RESOURCE_CONFIGS:
        raise ValueError(f"Resource configuration '{size}' not found")
    return DEFAULT_RESOURCE_CONFIGS[size]

def get_all_templates() -> List[Dict[str, Any]]:
    """Get all templates.
    
    Returns:
        List of all templates.
    """
    return DEFAULT_TEMPLATES