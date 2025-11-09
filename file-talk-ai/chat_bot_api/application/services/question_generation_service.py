"""
Question Generation Service
Handles generation of questions from PDF documents
"""
from typing import Optional
from config.env_config import config
from config.constants import AgentConstants
from .agent_service import AgentService
from .pdf_service import PDFService


class QuestionGenerationService(AgentService):
    """Service for generating questions from PDF documents"""

    def __init__(self):
        """Initialize question generation service"""
        super().__init__()
        self.pdf_service = PDFService()

    def generate_questions(
        self,
        document_url: str,
        min_page: Optional[int] = None,
        max_page: Optional[int] = None
    ) -> str:
        """
        Generate questions from PDF document

        Args:
            document_url: URL of the PDF document
            min_page: Minimum page number
            max_page: Maximum page number

        Returns:
            str: Generated questions and insights

        Raises:
            PDFDownloadError: If download fails
            PDFExtractionError: If extraction fails
            AgentProcessingError: If generation fails
        """
        self.log_info(
            "Processing question generation request",
            document_url=document_url,
            min_page=min_page,
            max_page=max_page
        )

        # Download and extract PDF text
        text = self.pdf_service.process_pdf(
            document_url,
            min_page=min_page,
            max_page=max_page,
            cleanup=True
        )

        # Create question generation agent
        agent = self.create_agent(
            name=AgentConstants.QUESTION_GEN_AGENT_NAME,
            description="Generates questions with Number and highlights key points from academic text.",
            role=AgentConstants.QUESTION_GEN_AGENT_ROLE,
            instructions=[
                f"Generate {config.QUESTIONS_COUNT} questions based on the input text.",
                "Identify the most important point from the text."
            ]
        )

        # Create generation prompt
        prompt = f"""
You are an educational assistant. Based on the following academic text:

{text}

Please do the following:
1. Generate {config.QUESTIONS_COUNT} thoughtful and relevant questions that test understanding of the content.
2. Highlight the most important concept or point from the text.
"""

        # Generate questions
        result = self.run_agent(agent, prompt)

        if not result or not result.strip():
            from chat_bot_api.domain.exceptions import AgentProcessingError
            raise AgentProcessingError("Empty response from question generation agent")

        return result
