# app/models/user.py

from sqlalchemy import Column, Integer, String
from app.models.base import Base

class User(Base):
    """
    User model for storing user account information.
    
    This model represents a user in the system with basic authentication fields.
    
    Attributes:
        id (int): Primary key, auto-incrementing user identifier
        email (str): Unique email address for user login, indexed for performance
        password_hash (str): Bcrypt hashed password for secure storage
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, doc="Unique user identifier")
    email = Column(String(255), unique=True, index=True, nullable=False, doc="User email address")
    password_hash = Column(String(255), nullable=False, doc="Bcrypt hashed password")

    def __repr__(self):
        """
        String representation of the User model.
        
        Returns:
            str: Human-readable representation of the user
        """
        return f"<User(id={self.id}, email={self.email})>"