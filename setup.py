"""Setup script for the Daytona Sandbox Orchestration Agent."""
from setuptools import setup, find_packages

setup(
    name="dagent",
    version="0.1.0",
    description="Daytona Sandbox Orchestration Agent",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "google-adk",  # ADK Python SDK
        "requests>=2.25.0",
        "pydantic>=1.8.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "dagent=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)