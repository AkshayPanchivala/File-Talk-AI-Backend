import os
import requests
import fitz  # PyMuPDF
from phi.agent import Agent
from phi.model.groq import Groq

# === Set Groq API Key ===
os.environ["GROQ_API_KEY"] = os.environ.get("groqApiKey")

PDF_FILE = "book.pdf"

class AgentMethods:
    @staticmethod
    def download_pdf(documentUrl):
        try:
            response = requests.get(documentUrl, timeout=10)
            response.raise_for_status()
            with open(PDF_FILE, "wb") as f:
                f.write(response.content)
            return {"success": True, "data": "✅ PDF downloaded."}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Error downloading PDF: {e}"}
        except IOError as e:
            return {"success": False, "error": f"File write error: {e}"}

    @staticmethod
    def extract_text_from_pdf(min_page=1, max_page=5):
        try:
            if not os.path.exists(PDF_FILE):
                return {"success": False, "error": f"The file '{PDF_FILE}' does not exist."}
            
            doc = fitz.open(PDF_FILE)
            full_text = ""
            total_pages = len(doc)

            min_page = max(min_page, 1)
            max_page = min(max_page, total_pages)

            if min_page > max_page:
                return {"success": False, "error": "Minimum page number cannot be greater than maximum page number."}

            for i in range(min_page - 1, max_page):
                page = doc.load_page(i)
                full_text += f"\n\n--- Page {i + 1} ---\n"
                full_text += page.get_text()

            return {"success": True, "data": full_text}
        except fitz.FileDataError as e:
            return {"success": False, "error": f"Invalid PDF file: {e}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error while extracting text: {e}"}

    @staticmethod
    def generate_questions_and_insights(text):
        try:
            # if not text or not text.strip():
            #     return {"success": False, "error": "Input text is empty."}

            agent = Agent(
                name="QuestionGenerator",
                description="Generates questions with Number and highlights key points from academic text.",
                role="PDF educational assistant",
                instructions=[
                    "Generate 20 questions based on the input text.",
                    "Identify the most important point from the text."
                ],
                model=Groq(id="llama3-70b-8192"),
                markdown=True
            )

            prompt = f"""
You are an educational assistant. Based on the following academic text:

{text}

Please do the following:
1. Generate 20 thoughtful and relevant questions that test understanding of the content.
2. Highlight the most important concept or point from the text.
"""
            response = agent.run(prompt)
            result = response.content.strip()

            if not result:
                return {"success": False, "error": "Empty response from model."}

            return {"success": True, "data": result}
        except Exception as e:
            return {"success": False, "error": f"Error generating questions: {e}"}
