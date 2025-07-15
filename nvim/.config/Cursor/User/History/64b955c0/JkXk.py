"""
SQLAlchemy models for PyDial.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from .db import Base
import enum

class User(Base):
    """User model for storing user account information."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    full_name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Relationships
    minute_balance = relationship("MinuteBalance", back_populates="user", uselist=False)
    call_history = relationship("CallHistory", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

class MinuteBalance(Base):
    """Model for tracking user's available calling minutes."""
    __tablename__ = 'minute_balances'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    minutes_available = Column(Float, default=0.0, nullable=False)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationship
    user = relationship("User", back_populates="minute_balance")

    def __repr__(self):
        return f"<MinuteBalance user_id={self.user_id} minutes={self.minutes_available}>"

class CallStatus(enum.Enum):
    """Enum for call status tracking."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class CallHistory(Base):
    """Model for tracking call history and outcomes."""
    __tablename__ = 'call_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    phone_number = Column(String(20), nullable=False)
    task_description = Column(Text, nullable=False)
    duration = Column(Float, default=0.0)  # Call duration in minutes
    status = Column(String(20), nullable=False, default=CallStatus.PENDING.value)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    outcome_summary = Column(Text)  # Summary of call results
    cost = Column(Float)  # Cost in minutes (might be different from duration due to pricing rules)
    
    # Relationship
    user = relationship("User", back_populates="call_history")

    def __repr__(self):
        return f"<CallHistory id={self.id} user_id={self.user_id} status={self.status}>"

# Helper functions for common queries
def get_user_by_email(session, email):
    """Get a user by their email address."""
    return session.query(User).filter(User.email == email).first()

def get_user_minute_balance(session, user_id):
    """Get a user's current minute balance."""
    balance = session.query(MinuteBalance).filter(MinuteBalance.user_id == user_id).first()
    return balance.minutes_available if balance else 0.0

def add_minutes_to_user(session, user_id, minutes):
    """Add minutes to a user's balance."""
    balance = session.query(MinuteBalance).filter(MinuteBalance.user_id == user_id).first()
    if balance:
        balance.minutes_available += minutes
    else:
        balance = MinuteBalance(user_id=user_id, minutes_available=minutes)
        session.add(balance)
    session.commit()

def deduct_minutes_from_user(session, user_id, minutes):
    """Deduct minutes from a user's balance."""
    balance = session.query(MinuteBalance).filter(MinuteBalance.user_id == user_id).first()
    if not balance or balance.minutes_available < minutes:
        raise ValueError("Insufficient minutes available")
    balance.minutes_available -= minutes
    session.commit()

def get_user_call_history(session, user_id, limit=10):
    """Get a user's recent call history."""
    return session.query(CallHistory)\
        .filter(CallHistory.user_id == user_id)\
        .order_by(CallHistory.started_at.desc())\
        .limit(limit)\
        .all() 