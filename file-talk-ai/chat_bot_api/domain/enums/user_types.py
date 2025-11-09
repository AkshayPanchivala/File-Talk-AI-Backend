"""
User Type Enums
Defines all possible user types in the system
"""
from enum import Enum


class UserTypeEnum(str, Enum):
    """Enumeration of user types"""

    USER = 'User'
    CHATBOT = 'Chatbot'
    SYSTEM = 'System'

    @classmethod
    def choices(cls):
        """Return choices for Django model field"""
        return [(item.value, item.name) for item in cls]

    @classmethod
    def values(cls):
        """Return list of all values"""
        return [item.value for item in cls]

    def __str__(self):
        return self.value
