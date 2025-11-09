"""
Database Models
Defines data models for the application
"""
from django.db import models
from django.contrib.auth.models import User
from chat_bot_api.domain.enums import ActionTypeEnum, UserTypeEnum


class BaseModel(models.Model):
    """Abstract base model with common fields"""

    created_at = models.DateTimeField(auto_now_add=True, help_text="Creation timestamp")
    updated_at = models.DateTimeField(auto_now=True, help_text="Last update timestamp")

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Document(BaseModel):
    """Model for tracking PDF documents"""

    url = models.URLField(max_length=500, help_text="URL of the PDF document")
    title = models.CharField(max_length=255, blank=True, null=True, help_text="Document title")
    file_hash = models.CharField(max_length=64, db_index=True, help_text="Hash of document URL")
    total_pages = models.IntegerField(null=True, blank=True, help_text="Total number of pages")
    file_size_bytes = models.BigIntegerField(null=True, blank=True, help_text="File size in bytes")

    class Meta:
        db_table = 'documents'
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        indexes = [
            models.Index(fields=['file_hash']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Document: {self.title or self.url[:50]}"


class ChatSession(BaseModel):
    """Model for chat sessions"""

    session_id = models.CharField(max_length=255, unique=True, db_index=True, help_text="Unique session identifier")
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='chat_sessions',
        help_text="Related document"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chat_sessions',
        help_text="User (if authenticated)"
    )
    is_active = models.BooleanField(default=True, help_text="Whether session is active")
    last_activity = models.DateTimeField(auto_now=True, help_text="Last activity timestamp")

    class Meta:
        db_table = 'chat_sessions'
        verbose_name = 'Chat Session'
        verbose_name_plural = 'Chat Sessions'
        indexes = [
            models.Index(fields=['session_id']),
            models.Index(fields=['is_active', 'last_activity']),
        ]

    def __str__(self):
        return f"Session: {self.session_id}"


class Conversation(BaseModel):
    """Model for conversation messages"""

    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='conversations',
        help_text="Related chat session"
    )
    action_type = models.CharField(
        max_length=50,
        choices=ActionTypeEnum.choices(),
        help_text="Type of action performed"
    )
    user_type = models.CharField(
        max_length=50,
        choices=UserTypeEnum.choices(),
        default=UserTypeEnum.USER.value,
        help_text="Type of user (User or Chatbot)"
    )
    content = models.TextField(help_text="Message content")
    metadata = models.JSONField(
        null=True,
        blank=True,
        help_text="Additional metadata (question, page range, etc.)"
    )

    class Meta:
        db_table = 'conversations'
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'
        indexes = [
            models.Index(fields=['session', 'created_at']),
            models.Index(fields=['action_type']),
        ]

    def __str__(self):
        return f"{self.user_type}: {self.content[:50]}"


class ProcessingLog(BaseModel):
    """Model for logging processing activities"""

    action_type = models.CharField(
        max_length=50,
        choices=ActionTypeEnum.choices(),
        help_text="Type of action"
    )
    document_url = models.URLField(max_length=500, help_text="Document URL")
    status = models.CharField(
        max_length=50,
        choices=[
            ('success', 'Success'),
            ('failed', 'Failed'),
            ('processing', 'Processing')
        ],
        default='processing',
        help_text="Processing status"
    )
    error_message = models.TextField(null=True, blank=True, help_text="Error message if failed")
    processing_time_ms = models.IntegerField(null=True, blank=True, help_text="Processing time in milliseconds")
    metadata = models.JSONField(null=True, blank=True, help_text="Additional processing metadata")

    class Meta:
        db_table = 'processing_logs'
        verbose_name = 'Processing Log'
        verbose_name_plural = 'Processing Logs'
        indexes = [
            models.Index(fields=['action_type', 'status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.action_type} - {self.status}"
