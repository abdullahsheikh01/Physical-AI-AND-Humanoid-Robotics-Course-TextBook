from typing import Dict, Optional, List
from datetime import datetime, timedelta
from ..models.chat_models import ConversationSession
import uuid


class SessionService:
    """
    Service for managing conversation sessions
    """
    def __init__(self):
        # In-memory storage for sessions (in production, use Redis or database)
        self.sessions: Dict[str, ConversationSession] = {}
        # Session timeout in minutes
        self.session_timeout = 30

    def create_session(self, user_id: Optional[str] = None) -> ConversationSession:
        """
        Create a new conversation session
        """
        session_id = str(uuid.uuid4())
        session = ConversationSession(
            session_id=session_id,
            user_id=user_id
        )
        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[ConversationSession]:
        """
        Get an existing conversation session
        """
        if session_id in self.sessions:
            session = self.sessions[session_id]
            # Check if session has expired
            if self._is_session_expired(session):
                self.delete_session(session_id)
                return None
            return session
        return None

    def update_session(self, session_id: str, query: str, response: str) -> Optional[ConversationSession]:
        """
        Update a session with a new query-response pair
        """
        session = self.get_session(session_id)
        if session:
            # Add the query-response pair to history
            session.history.append({
                "query": query,
                "response": response,
                "timestamp": datetime.now().isoformat()
            })
            session.last_interaction = datetime.now()
            self.sessions[session_id] = session
            return session
        return None

    def delete_session(self, session_id: str):
        """
        Delete a conversation session
        """
        if session_id in self.sessions:
            del self.sessions[session_id]

    def _is_session_expired(self, session: ConversationSession) -> bool:
        """
        Check if a session has expired based on timeout
        """
        time_diff = datetime.now() - session.last_interaction
        return time_diff > timedelta(minutes=self.session_timeout)

    def clear_expired_sessions(self):
        """
        Remove all expired sessions
        """
        expired_sessions = []
        for session_id, session in self.sessions.items():
            if self._is_session_expired(session):
                expired_sessions.append(session_id)

        for session_id in expired_sessions:
            self.delete_session(session_id)


# Global session service instance
session_service = SessionService()