#!/usr/bin/env python
"""Entry point script for running the Daytona Sandbox Orchestration Agent."""
import os
import sys
import logging
import argparse

# Add src directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from src.main import main

if __name__ == "__main__":
    main()