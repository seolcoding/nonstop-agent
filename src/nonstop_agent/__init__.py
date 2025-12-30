"""
Nonstop Agent - Long-running autonomous agent harness for Claude.

A framework for building autonomous agents that work continuously
across multiple sessions, inspired by Anthropic's best practices.
"""

__version__ = "0.1.0"

from .agent import run_autonomous_agent
from .client import create_client
from .security import bash_security_hook

__all__ = [
    "run_autonomous_agent",
    "create_client",
    "bash_security_hook",
]
