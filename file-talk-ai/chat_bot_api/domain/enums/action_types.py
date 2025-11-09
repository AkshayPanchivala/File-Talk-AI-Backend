"""
Action Type Enums
Defines all possible conversation action types
"""
from enum import Enum


class ActionTypeEnum(str, Enum):
    """Enumeration of action types for conversation handling"""

    QUESTION_ANSWER = 'question_answer'
    SUMMARIZER = 'summarizer'
    GENERATE_QUESTIONS = 'generate_questions'

    @classmethod
    def choices(cls):
        """Return choices for Django model field"""
        return [(item.value, item.name) for item in cls]

    @classmethod
    def values(cls):
        """Return list of all values"""
        return [item.value for item in cls]

    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Check if value is a valid action type"""
        return value in cls.values()

    def __str__(self):
        return self.value
