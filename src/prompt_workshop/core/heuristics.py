"""Heuristic analyzer for prompt behavior patterns."""

import re
from typing import TypedDict


class HeuristicFlags(TypedDict):
    """Flags for detected heuristic patterns."""
    tool_announcement: bool
    verbose_no_tools: bool
    menu_pattern: bool


class HeuristicsAnalyzer:
    """Analyze responses for heuristic patterns."""

    ANNOUNCEMENT_PATTERNS = [
        r"(?i)I will now",
        r"(?i)Let me",
        r"(?i)I'm going to",
        r"(?i)I'll proceed to",
    ]

    MENU_PATTERNS = [
        r"Option [A-D1-4]:",
        r"(?:Here are|These are) (?:some|the) options",
        r"\d+\.\s+\*\*[^*]+\*\*",
    ]

    def __init__(self, profile: str = "coding"):
        """
        Initialize analyzer for a specific profile.

        Args:
            profile: Profile name (currently only 'coding' supported)
        """
        self.profile = profile

    def analyze(self, response_text: str, token_count: int, tool_call_count: int) -> HeuristicFlags:
        """
        Analyze a response for heuristic patterns.

        Args:
            response_text: The actual response text from the model
            token_count: Number of tokens in the response
            tool_call_count: Number of tool calls in the response

        Returns:
            Dictionary of detected flags
        """
        flags: HeuristicFlags = {
            "tool_announcement": False,
            "verbose_no_tools": False,
            "menu_pattern": False,
        }

        if self.profile == "coding":
            flags.update(self._analyze_coding(response_text, token_count, tool_call_count))

        return flags

    def _analyze_coding(self, response_text: str, token_count: int, tool_call_count: int) -> HeuristicFlags:
        """Analyze coding-specific patterns."""
        flags: HeuristicFlags = {
            "tool_announcement": False,
            "verbose_no_tools": False,
            "menu_pattern": False,
        }

        # Check for tool announcements
        for pattern in self.ANNOUNCEMENT_PATTERNS:
            if re.search(pattern, response_text):
                flags["tool_announcement"] = True
                break

        # Check for verbose responses without tools
        if token_count > 8000 and tool_call_count == 0:
            flags["verbose_no_tools"] = True

        # Check for menu patterns
        for pattern in self.MENU_PATTERNS:
            if re.search(pattern, response_text):
                flags["menu_pattern"] = True
                break

        return flags

    def check_flags(self, flags: HeuristicFlags) -> list[str]:
        """Return list of detected issues."""
        issues = []
        if flags["tool_announcement"]:
            issues.append("tool_announcement")
        if flags["verbose_no_tools"]:
            issues.append("verbose_no_tools")
        if flags["menu_pattern"]:
            issues.append("menu_pattern")
        return issues
