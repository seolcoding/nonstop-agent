"""
Progress Tracking Utilities
===========================

Functions for tracking and displaying progress of the autonomous agent.
"""

import json
from pathlib import Path


SESSION_FILE = "claude_session.json"


def count_passing_tests(project_dir: Path) -> tuple[int, int]:
    """
    Count passing and total tests in feature_list.json.

    Args:
        project_dir: Directory containing feature_list.json

    Returns:
        (passing_count, total_count)
    """
    tests_file = project_dir / "feature_list.json"

    if not tests_file.exists():
        return 0, 0

    try:
        with open(tests_file, "r") as f:
            tests = json.load(f)

        total = len(tests)
        passing = sum(1 for test in tests if test.get("passes", False))

        return passing, total
    except (json.JSONDecodeError, IOError):
        return 0, 0


def print_session_header(session_num: int, session_type: str) -> None:
    """Print a formatted header for the session."""
    type_labels = {
        "analysis": "EXISTING PROJECT ANALYSIS",
        "initializer": "INITIALIZER AGENT",
        "coding": "CODING AGENT",
    }
    label = type_labels.get(session_type, session_type.upper())

    print("\n" + "=" * 70)
    print(f"  SESSION {session_num}: {label}")
    print("=" * 70)
    print()


def print_progress_summary(project_dir: Path) -> None:
    """Print a summary of current progress."""
    passing, total = count_passing_tests(project_dir)

    if total > 0:
        percentage = (passing / total) * 100
        print(f"\nProgress: {passing}/{total} tests passing ({percentage:.1f}%)")
    else:
        print("\nProgress: feature_list.json not yet created")


def save_session_id(project_dir: Path, session_id: str) -> None:
    """Save session ID for later resumption."""
    session_file = project_dir / SESSION_FILE
    try:
        with open(session_file, "w") as f:
            json.dump({"session_id": session_id}, f)
    except IOError as e:
        print(f"Warning: Could not save session ID: {e}")


def load_session_id(project_dir: Path) -> str | None:
    """Load saved session ID."""
    session_file = project_dir / SESSION_FILE
    if session_file.exists():
        try:
            with open(session_file) as f:
                data = json.load(f)
                return data.get("session_id")
        except (json.JSONDecodeError, IOError):
            pass
    return None
