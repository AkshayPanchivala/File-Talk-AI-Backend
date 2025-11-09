import os
import logging
import tempfile
import requests
import fitz  # PyMuPDF
from phi.agent import Agent
from phi.model.groq import Groq

logger = logging.getLogger(__name__)

os.environ["GROQ_API_KEY"] = os.environ.get("groqApiKey")

class QuestionAnswerService:
    """
    PDF-based QA service for Groq models.
    Uses direct text extraction (PyMuPDF) for reliability.
    """

    def __init__(self):
        self.model_id = "llama-3.3-70b-versatile"

    def download_pdf(self, url: str) -> str:
        """Download the PDF and return its local path."""
        try:
            logger.info(f"Downloading PDF from {url}")
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            for chunk in response.iter_content(1024):
                temp_file.write(chunk)
            temp_file.close()
            logger.info(f"✅ PDF downloaded to {temp_file.name}")
            return temp_file.name
        except Exception as e:
            logger.error(f"❌ Failed to download PDF: {e}")
            raise RuntimeError("Failed to download PDF") from e

    def extract_pdf_text(self, file_path: str) -> str:
        """Extract readable text from a PDF file using PyMuPDF."""
        try:
            logger.info(f"Extracting text from {file_path}")
            pdf_document = fitz.open(file_path)
            text = ""
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                text += page.get_text("text") + "\n\n"

            pdf_document.close()
            os.remove(file_path)  # cleanup temp file

            if not text.strip():
                raise ValueError("No text found in the PDF.")

            # Limit text size for Groq model safety
            if len(text) > 100000:
                text = text[:100000] + "\n\n...[Content truncated for model limit]..."

            logger.info("✅ Text extracted successfully.")
            return text

        except Exception as e:
            logger.error(f"❌ Error extracting text from PDF: {e}")
            raise RuntimeError("Failed to extract text from PDF") from e

    def initialize_agent(self, pdf_text: str):
        """Initialize Groq QA agent with PDF context."""
        try:
            logger.info("Initializing Groq QA agent with PDF context...")
            context_prompt = (
                "You are an AI assistant that answers questions using **only** "
                "the following PDF content. Do not use external knowledge, "
                "inference, or assumptions. If the answer cannot be found, say: "
                "'I'm sorry, but I couldn't find the answer to your question in the provided PDF document.'\n\n"
                "=== PDF CONTENT START ===\n"
                f"{pdf_text}\n"
                "=== PDF CONTENT END ==="
            )

            agent = Agent(
                description=context_prompt,
                model=Groq(id=self.model_id),
                markdown=True,
                fallback_messages=[
                    "I'm sorry, but I couldn't find the answer to your question in the provided PDF document."
                ],
            )
            return agent
        except Exception as e:
            logger.error(f"❌ Error initializing agent: {e}")
            raise RuntimeError("Failed to initialize agent") from e

    def ask_question(self, agent, question: str) -> str:
        """Ask a question and return the answer."""
        try:
            logger.info(f"Asking: {question}")
            response = agent.run(question)
            answer = response.content.strip()

            if not answer or "I'm sorry" in answer:
                return "I'm sorry, but I couldn't find the answer to your question in the provided PDF document."

            return answer
        except Exception as e:
            logger.error(f"❌ Error processing question: {e}")
            return "Error processing the question."

    def answer_question(self, document_url: str, question: str) -> str:
        """Full workflow."""
        logger.info("Starting question answering process (direct PDF mode)...")
        local_pdf = self.download_pdf(document_url)
        pdf_text = self.extract_pdf_text(local_pdf)
        agent = self.initialize_agent(pdf_text)
        return self.ask_question(agent, question)
