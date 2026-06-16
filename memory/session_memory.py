"""
Day 1 Memory: In-session key-value store.
Day 3 will upgrade this to ChromaDB for persistent memory across sessions.
"""

from datetime import datetime


class SessionMemory:
    """
    Simple in-session memory store.
    Stores facts about the user extracted from the conversation.
    """

    def __init__(self):
        self._store: dict = {}
        self._timestamps: dict = {}

    def update(self, key: str, value: str):
        """Store or update a memory entry."""
        self._store[key] = value
        self._timestamps[key] = datetime.now().strftime("%H:%M")

    def get(self, key: str) -> str | None:
        """Retrieve a single memory entry."""
        return self._store.get(key)

    def get_all(self) -> dict:
        """Return all stored memories."""
        return dict(self._store)

    def delete(self, key: str):
        """Remove a memory entry."""
        self._store.pop(key, None)
        self._timestamps.pop(key, None)

    def clear(self):
        """Wipe all memory."""
        self._store.clear()
        self._timestamps.clear()

    def to_context_string(self) -> str:
        """
        Format memory as a context string to inject into prompts.
        Used when building prompts for Gemini.
        """
        if not self._store:
            return ""
        lines = ["[What I know about this user:]"]
        for key, value in self._store.items():
            lines.append(f"- {key}: {value}")
        return "\n".join(lines)