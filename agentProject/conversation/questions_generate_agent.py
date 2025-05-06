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
        url = documentUrl
        response = requests.get(url)
        with open(PDF_FILE, "wb") as f:
            f.write(response.content)
        print("✅ PDF downloaded.")

    @staticmethod
    def extract_text_from_pdf(min_page=1, max_page=5):
        try:
            doc = fitz.open(PDF_FILE)
            full_text = ""
            total_pages = len(doc)

            # Validate page bounds
            min_page = max(min_page, 1)
            max_page = min(max_page, total_pages)

            for i in range(min_page - 1, max_page):
                page = doc.load_page(i)
                full_text += f"\n\n--- Page {i + 1} ---\n"
                full_text += page.get_text()

            print(f"📄 Extracted text from pages {min_page} to {max_page}.")
            return full_text
        except Exception as e:
            print(f"❌ Error extracting PDF text: {e}")
            raise

    @staticmethod
    def generate_questions_and_insights(text):
        try:
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
            return result
        except Exception as e:
            print(f"❌ Error generating questions: {e}")
            raise

