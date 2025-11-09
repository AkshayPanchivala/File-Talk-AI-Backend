"""
Summary Service
Handles PDF document summarization
"""
from typing import Optional
from config.env_config import config
from config.constants import AgentConstants
from .agent_service import AgentService
from .pdf_service import PDFService


class SummaryService(AgentService):
    """Service for summarizing PDF documents"""

    def __init__(self):
        """Initialize summary service"""
        super().__init__()
        self.pdf_service = PDFService()

    def summarize_document(
        self,
        document_url: str,
        min_page: Optional[int] = None,
        max_page: Optional[int] = None
    ) -> str:
        """
        Summarize PDF document

        Args:
            document_url: URL of the PDF document
            min_page: Minimum page number
            max_page: Maximum page number

        Returns:
            str: Document summary

        Raises:
            PDFDownloadError: If download fails
            PDFExtractionError: If extraction fails
            AgentProcessingError: If summarization fails
        """
        self.log_info(
            "Processing document summarization request",
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

        # Create summarization agent
        agent = self.create_agent(
            name=AgentConstants.SUMMARY_AGENT_NAME,
            description=f"Summarizes a PDF document in a minimum of {config.SUMMARY_MIN_WORDS} words.",
            role=AgentConstants.SUMMARY_AGENT_ROLE,
            instructions=[
                f"Provide a clear, structured summary with at least {config.SUMMARY_MIN_WORDS} words.",
                "Use headings and bullet points where appropriate."
            ]
        )

        # Create summarization prompt
        prompt = f"""
You are a professional summarizer AI. Summarize the following academic content in **at least {config.SUMMARY_MIN_WORDS} words**. Ensure clarity, depth, and structure with sections, bullet points, and examples if relevant.

{text}
"""

        # Generate summary
        summary = self.run_agent(agent, prompt)

        if not summary or not summary.strip():
            from chat_bot_api.domain.exceptions import AgentProcessingError
            raise AgentProcessingError("Empty response from summarization agent")

        return summary
