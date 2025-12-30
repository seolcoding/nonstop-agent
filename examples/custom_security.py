#!/usr/bin/env python3
"""
Custom Security Example
=======================

Demonstrates how to customize the security settings.
"""

from nonstop_agent.security import (
    add_allowed_command,
    remove_allowed_command,
    ALLOWED_COMMANDS,
)


def setup_custom_security():
    """Configure custom allowed commands."""

    # Add Docker commands
    add_allowed_command("docker")
    add_allowed_command("docker-compose")

    # Add Rust/Cargo commands
    add_allowed_command("cargo")
    add_allowed_command("rustc")

    # Add Go commands
    add_allowed_command("go")

    # Remove a command if needed
    # remove_allowed_command("pkill")

    # Print current allowed commands
    print("Current allowed commands:")
    for cmd in sorted(ALLOWED_COMMANDS):
        print(f"  - {cmd}")


if __name__ == "__main__":
    setup_custom_security()
