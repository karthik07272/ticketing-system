from sqlalchemy import Column, Integer, String, Text, DateTime, Index, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import uuid

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(500), nullable=False, index=True)
    body = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="open", index=True)
    priority = Column(String(20), nullable=False, default="medium", index=True)
    customer_email = Column(String(255), nullable=False, index=True)
    customer_name = Column(String(255), nullable=False, index=True)
    assigned_agent = Column(String(255), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # PostgreSQL-specific optimizations
    __table_args__ = (
        # Composite indexes for better performance
        Index('idx_tickets_status_priority', 'status', 'priority'),
        Index('idx_tickets_created_at_status', 'created_at', 'status'),
        Index('idx_tickets_customer_email_status', 'customer_email', 'status'),
        Index('idx_tickets_assigned_agent_status', 'assigned_agent', 'status'),
        
        # Full-text search indexes or fuzzy string matching,(PostgreSQL specific)
        Index('idx_tickets_subject_gin', 'subject', postgresql_using='gin', postgresql_ops={'subject': 'gin_trgm_ops'}),
        Index('idx_tickets_body_gin', 'body', postgresql_using='gin', postgresql_ops={'body': 'gin_trgm_ops'}),
        Index('idx_tickets_customer_name_gin', 'customer_name', postgresql_using='gin', postgresql_ops={'customer_name': 'gin_trgm_ops'}),
    )

class ChatSession(Base):
    """Store chat sessions for better context tracking"""
    __tablename__ = "chat_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(String(255), nullable=True, index=True)
    session_data = Column(Text, nullable=True)  # JSON data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True, index=True)

class ChatMessage(Base):
    """Store chat messages for analytics and improvement"""
    __tablename__ = "chat_messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    session_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    user_id = Column(String(255), nullable=True, index=True)
    message_type = Column(String(20), nullable=False, index=True)
    content = Column(Text, nullable=False)
    intent_type = Column(String(50), nullable=True, index=True)
    intent_confidence = Column(String(10), nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    __table_args__ = (
        Index('idx_chat_messages_session_created', 'session_id', 'created_at'),
        Index('idx_chat_messages_user_created', 'user_id', 'created_at'),
        Index('idx_chat_messages_intent_created', 'intent_type', 'created_at'),
    )
