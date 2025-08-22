import sqlite3
from datetime import datetime

class AgentMemory:
    def __init__(self, db_path='research_agent.db'):
        """
        Initializes the AgentMemory instance.

        Args:
            db_path (str): The path to the SQLite database file.
        """
        self.db_path = db_path

    def _get_connection(self):
        """Returns a new database connection."""
        return sqlite3.connect(self.db_path)

    def save_entry(self, project_id: str, agent_name: str, action: str, content: str):
        """
        Saves a new entry to the agent_memory table.

        Args:
            project_id (str): The ID of the project.
            agent_name (str): The name of the agent.
            action (str): The action performed by the agent.
            content (str): The content related to the action.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO agent_memory (project_id, agent_name, action, content)
                    VALUES (?, ?, ?, ?)
                    """,
                    (project_id, agent_name, action, content)
                )
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def get_context(self, project_id: str, limit: int = 10) -> str:
        """
        Retrieves the last N entries for a given project to form a context string.

        Args:
            project_id (str): The ID of the project.
            limit (int): The maximum number of memory entries to retrieve.

        Returns:
            str: A formatted string of recent memory entries.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT timestamp, agent_name, action, content
                    FROM agent_memory
                    WHERE project_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                    """,
                    (project_id, limit)
                )
                rows = cursor.fetchall()

            if not rows:
                return "No recent memory entries found."

            # Format the memories into a string
            formatted_memory = "Recent Memory Entries (most recent first):\n"
            for row in reversed(rows):  # Reverse to show oldest first in the context
                timestamp, agent_name, action, content = row
                formatted_memory += f"- [{timestamp}] {agent_name} {action}: {content}\n"

            return formatted_memory
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return "Error retrieving memory."
