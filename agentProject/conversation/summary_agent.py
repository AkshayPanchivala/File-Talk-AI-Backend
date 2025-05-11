import os
import requests
import fitz  # PyMuPDF
from phi.agent import Agent
from phi.model.groq import Groq

# === Set Groq API Key ===
os.environ["GROQ_API_KEY"] = os.environ.get("groqApiKey")

PDF_FILE = "book.pdf"  # Correct file extension

class AnswerGenrate:
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
            return {"success": False, "error": f"Error writing PDF file: {e}"}

    @staticmethod
    def extract_text_from_pdf(min_page=1, max_page=5):
        try:
            if not os.path.exists(PDF_FILE):
                return {"success": False, "error": f"The file '{PDF_FILE}' does not exist."}
            doc = fitz.open(PDF_FILE)
            total_pages = len(doc)
            min_page = max(min_page, 1)
            max_page = min(max_page, total_pages)
            if min_page > max_page:
                return {"success": False, "error": "Minimum page number cannot be greater than maximum."}

            full_text = ""

            for i in range(min_page - 1, max_page):
                page = doc.load_page(i)
                full_text += f"\n\n--- Page {i + 1} ---\n"
                full_text += page.get_text()
              
            return {"success": True, "data": full_text}
        except fitz.FileDataError as e:
            return {"success": False, "error": f"Invalid PDF file: {e}"}
        except Exception as e:
            return {"success": False, "error": f"Error extracting PDF text: {e}"}

    @staticmethod
    def summarize_text_with_agent(text):
        try:
           
            # print("Text content:", text.strip())  # Print first 1000 characters for debugging
            # if not text or not text.strip():
            #     print("Input text is empty or invalid for summarization.")
            #     return {"success": False, "error": "Input text is empty or invalid for summarization."}

            agent = Agent(
                name="Summarizer",
                description="Summarizes a PDF document in a minimum of 8000 words.",
                role="PDF summarizer",
                instructions=[
                    "Provide a clear, structured summary with at least 8000 words.",
                    "Use headings and bullet points where appropriate."
                ],
                model=Groq(id="llama3-70b-8192"),
                markdown=True,
                # debug_mode=True,
            )

            prompt = f"""
You are a professional summarizer AI. Summarize the following academic content in **at least 8000 words**. Ensure clarity, depth, and structure with sections, bullet points, and examples if relevant.

{text}
"""      
            response = agent.run(prompt)
# If response is a dict, safely extract the 'content'
            if isinstance(response, dict):
                summary = response.get("content", "").strip()
            else:
                summary = getattr(response, "content", "").strip()

            if not summary:
                return {"success": False, "error": "Empty response from the summarization agent."}
            if not summary:
                return {"success": False, "error": "Empty response from the summarization agent."}

            return {"success": True, "data": summary}
        except Exception as e:
            return {"success": False, "error": f"Error generating summary: {e}"}
