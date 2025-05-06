import os
import requests
import fitz  # PyMuPDF
from phi.agent import Agent
from phi.model.groq import Groq

# === Set Groq API Key ===
os.environ["GROQ_API_KEY"] = os.environ.get("groqApiKey")

PDF_FILE = "book.pdf"  # ✅ Corrected from book.txt

# === Download the PDF ===
class AnswerGenrate():
    @staticmethod
    def download_pdf(documentUrl):
        url = documentUrl
        response = requests.get(url)
        with open(PDF_FILE, "wb") as f:
            f.write(response.content)
        print("✅ PDF downloaded.")

    # === Extract text from specified pages ===
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
            exit(1)

    # === Summarize the extracted text ===
    @staticmethod
    def summarize_text_with_agent(text):
        try:
            agent = Agent(
                name="Summarizer",
                description="Summarizes a PDF document in a minimum of 8000 words.",
                role="PDF summarizer",
                instructions=[
                    "Provide a clear, structured summary with at least 8000 words.",
                    "Use headings and bullet points where appropriate."
                ],
                model=Groq(id="llama3-70b-8192"),
                markdown=True
            )

            prompt = f"""
    You are a professional summarizer AI. Summarize the following academic content in **at least 8000 words**. Ensure clarity, depth, and structure with sections, bullet points, and examples if relevant.

    {text}
    """
            response = agent.run(prompt)
            summary = response.content.strip()

            with open("full_pdf_summary.txt", "w", encoding="utf-8") as f:
                f.write(summary)

            print("✅ Summary generated.")
            print(f"📄 Length: {len(summary)} characters")
            print(summary)
            return summary
        except Exception as e:
            print(f"❌ Error generating summary: {e}")
            exit(1)

# # === Main logic ===
# def main():
#     if not os.path.exists(PDF_FILE):
#         AnswerGenrate.download_pdf()
#     text = AnswerGenrate.extract_text_from_pdf()
#     AnswerGenrate.summarize_text_with_agent(text)

# if __name__ == "__main__":
#     main()
