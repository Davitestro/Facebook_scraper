"""Utility helpers for managing a pool of user-agent strings."""

import os
from typing import List, Optional


class UserAgentManager:
    """Load user agents from a configured file."""

    def __init__(self, user_agent_file: Optional[str] = None):
        self.user_agent_file = user_agent_file or os.path.join("config", "user_agents.txt")
        self.user_agents = self._load_user_agents()
        self._index = 0

    def _load_user_agents(self) -> List[str]:
        if not os.path.exists(self.user_agent_file):
            return [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            ]

        with open(self.user_agent_file, "r", encoding="utf-8") as handle:
            return [line.strip() for line in handle if line.strip()]

    def get_user_agent(self) -> str:
        if not self.user_agents:
            return "Mozilla/5.0"

        user_agent = self.user_agents[self._index % len(self.user_agents)]
        self._index += 1
        return user_agent

    def reset(self) -> None:
        self._index = 0
