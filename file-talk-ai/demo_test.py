"""
Demo Test Script for PDF Question-Answer System
Run this standalone script to test the core functionality

Usage:
    python demo_test.py
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Setup Django
import django
django.setup()

from chat_bot_api.application.services.question_answer_service import QuestionAnswerService


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_result(question, answer):
    """Print formatted result"""
    print(f"Question: {question}")
    print(f"\nAnswer:\n{answer}")
    print("\n" + "-" * 70)


def main():
    """Run demo tests"""

    print_header("PDF Question-Answer System - Demo Test")

    # Initialize service
    print("Initializing Question-Answer Service...")
    qa_service = QuestionAnswerService()
    print("✓ Service initialized successfully\n")

    # Test PDF - replace with your actual PDF path or URL
    # For demo: Use a sample resume or any PDF file
    pdf_path = input("Enter path to PDF file (or press Enter to use default): ").strip()

    if not pdf_path:
        # Try to find a sample PDF in the project
        sample_paths = [
            "sample_resume.pdf",
            "test_document.pdf",
            "demo.pdf"
        ]

        for path in sample_paths:
            if Path(path).exists():
                pdf_path = path
                break

        if not pdf_path:
            print("\n⚠ No sample PDF found. Please provide a PDF file path.")
            print("You can:")
            print("1. Create a file named 'sample_resume.pdf' in the project root")
            print("2. Provide a URL to a PDF file")
            print("3. Provide a local file path")
            return

    print(f"\nUsing PDF: {pdf_path}")

    # Test questions
    test_questions = [
        "What are the key skills mentioned in this document?",
        "What is the main topic of this document?",
        "Summarize the most important information from this document."
    ]

    # Allow custom question
    print("\n" + "=" * 70)
    custom_question = input("Enter your question (or press Enter to use default questions): ").strip()

    if custom_question:
        test_questions = [custom_question]

    # Process questions
    print_header("Processing Questions")

    for i, question in enumerate(test_questions, 1):
        print(f"\n[Test {i}/{len(test_questions)}]")
        print(f"Question: {question}")
        print("\nProcessing... (this may take a few seconds)")

        try:
            answer = qa_service.answer_question(
                document_url=pdf_path,
                question=question
            )

            print(f"\n✓ Answer received:")
            print("-" * 70)
            print(answer)
            print("-" * 70)

        except Exception as e:
            print(f"\n✗ Error: {str(e)}")
            print(f"Error type: {type(e).__name__}")

    print_header("Demo Test Completed")
    print("✓ All tests executed")
    print("\nNext steps:")
    print("1. Start Django server: python manage.py runserver")
    print("2. Test via API: POST to /api/v1/question-answer/")
    print("3. See DEMO_SCRIPT.md for video recording instructions")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Test interrupted by user")
    except Exception as e:
        print(f"\n\n✗ Fatal error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
