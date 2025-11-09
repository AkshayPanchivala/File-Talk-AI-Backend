# File Talk AI - Backend

A Django-based backend API for interacting with PDF documents using AI. This application leverages GROQ's LLM to provide intelligent document analysis, question answering, summarization, and question generation capabilities.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Configuration](#environment-configuration)
- [API Documentation](#api-documentation)
- [Frontend Repository](#frontend-repository)
- [License](#license)

---

## Features

- **Question Answering**: Ask questions about your PDF documents and get AI-powered answers
- **Document Summarization**: Generate concise summaries of PDF content (configurable page ranges)
- **Question Generation**: Automatically generate relevant questions from document content
- **PDF Processing**: Upload and process PDF files with text extraction
- **RESTful API**: Clean, versioned API endpoints (v1)
- **Enterprise Architecture**: Domain-driven design with clear separation of concerns
- **Comprehensive Error Handling**: Custom exceptions with detailed error responses
- **Configurable AI Models**: Support for different GROQ model configurations
- **Logging & Monitoring**: Structured logging with JSON/text format support

---

## Architecture

This project follows **Clean Architecture** principles with the following layers:

```
chat_bot_api/
├── api/                    # API Layer (Controllers)
│   ├── middlewares/        # Custom middleware
│   └── v1/                 # API version 1
│       ├── views.py        # Request handlers
│       ├── serializers.py  # Input validation
│       └── validators.py   # Custom validators
│
├── application/            # Application Layer (Use Cases)
│   ├── dto/                # Data Transfer Objects
│   │   ├── request_dto.py  # Request DTOs
│   │   └── response_dto.py # Response DTOs
│   ├── services/           # Business logic services
│   │   ├── agent_service.py              # AI agent orchestration
│   │   ├── question_answer_service.py    # Q&A service
│   │   ├── summary_service.py            # Summarization service
│   │   └── question_generation_service.py # Question generation
│   └── use_cases/          # Application use cases
│
├── domain/                 # Domain Layer (Business Logic)
│   ├── enums/              # Enumerations
│   │   ├── action_types.py # Action type enums
│   │   └── user_types.py   # User type enums
│   ├── exceptions/         # Custom exceptions
│   │   ├── base.py         # Base exception classes
│   │   ├── agent_exceptions.py
│   │   └── pdf_exceptions.py
│   └── models/             # Domain models
│
├── infrastructure/         # Infrastructure Layer
│   ├── cache/              # Caching implementations
│   ├── external/           # External service integrations
│   ├── repositories/       # Data access layer
│   └── storage/            # File storage (local/S3)
│
├── core/                   # Core Utilities
│   ├── decorators/         # Custom decorators (e.g., retry)
│   ├── mixins/             # Reusable mixins
│   └── utils/              # Helper utilities
│       ├── logger.py       # Logging utilities
│       ├── helpers.py      # General helpers
│       └── validators.py   # Validation utilities
│
└── tests/                  # Test Suite
    ├── unit/               # Unit tests
    └── integration/        # Integration tests
```

---

## Tech Stack

**Framework & Core**
- Django 4.2+
- Django REST Framework
- Django CORS Headers

**AI & ML**
- Phidata - AI agent framework
- GROQ API - LLM inference

**PDF Processing**
- PyMuPDF (fitz) - PDF text extraction

**Database**
- SQLite (development)
- PostgreSQL support (production-ready)

**Production Tools**
- Gunicorn - WSGI server
- WhiteNoise - Static file serving
- python-dotenv - Environment management

---

## Project Structure

```
file-talk-ai/
├── chat_bot_api/           # Main application
├── config/                 # Configuration module
│   ├── env_config.py       # Environment configuration
│   ├── constants.py        # Application constants
│   └── settings/           # Django settings
├── file_talk_ai_project/   # Django project settings
├── media/                  # Uploaded files (gitignored)
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── .env.example            # Environment variables template
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)
- GROQ API key ([Get one here](https://console.groq.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AkshayPanchivala/File-Talk-AI-Backend.git
   cd File-Talk-AI-Backend-main/file-talk-ai
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Create .env file (see Environment Configuration section)
   cp .env.example .env
   # Edit .env and add your GROQ API key
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000`

---

## Environment Configuration

Create a `.env` file in the project root (`file-talk-ai/`) directory:

```env
# ===================================
# Required Configuration
# ===================================
groqApiKey=your_groq_api_key_here

# ===================================
# AI Model Configuration (Optional)
# ===================================
GROQ_MODEL_ID=llama-3.3-70b-versatile
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=8000

# ===================================
# PDF Processing (Optional)
# ===================================
PDF_DOWNLOAD_TIMEOUT=30
PDF_MAX_PAGES=100
PDF_DEFAULT_MIN_PAGE=1
PDF_DEFAULT_MAX_PAGE=5
PDF_STORAGE_PATH=media/pdfs

# ===================================
# Summary Configuration (Optional)
# ===================================
SUMMARY_MIN_WORDS=8000

# ===================================
# Question Generation (Optional)
# ===================================
QUESTIONS_COUNT=20

# ===================================
# Cache Configuration (Optional)
# ===================================
CACHE_ENABLED=False
CACHE_TTL=3600
REDIS_URL=redis://localhost:6379/0

# ===================================
# Storage Configuration (Optional)
# ===================================
STORAGE_BACKEND=local  # Options: local, s3
# AWS_ACCESS_KEY_ID=your_aws_access_key
# AWS_SECRET_ACCESS_KEY=your_aws_secret_key
# AWS_STORAGE_BUCKET_NAME=your_bucket_name
# AWS_S3_REGION_NAME=us-east-1

# ===================================
# Logging Configuration (Optional)
# ===================================
LOG_LEVEL=INFO          # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=json         # Options: json, text

# ===================================
# Feature Flags (Optional)
# ===================================
ENABLE_RATE_LIMITING=False
ENABLE_MONITORING=False

# ===================================
# Environment (Optional)
# ===================================
ENVIRONMENT=development # Options: development, testing, production
DEBUG=True
```

### Getting Your GROQ API Key

1. Visit [GROQ Console](https://console.groq.com/)
2. Sign up or log in to your account
3. Navigate to **API Keys** section
4. Click **Create API Key**
5. Copy the generated key
6. Add it to your `.env` file

---

## API Documentation

### Base URL
```
http://localhost:8000/api/v1/chat-bot/
```

### Endpoints

#### 1. Get API Information
```http
GET /api/v1/chat-bot/conversation/
```

**Response:**
```json
{
  "message": "File Talk AI - Conversation API",
  "version": "v1",
  "endpoints": {
    "POST /conversation/": "Process conversation",
    "POST /options/": "Get available options"
  }
}
```

#### 2. Process Conversation (Question Answering)
```http
POST /api/v1/chat-bot/conversation/
Content-Type: application/json
```

**Request Body:**
```json
{
  "action": "question_answer",
  "documentUrl": "https://example.com/document.pdf",
  "question": "What is the main topic of this document?"
}
```

**Response:**
```json
{
  "data": "The main topic of this document is...",
  "message": "Question answered successfully"
}
```

#### 3. Document Summarization
```http
POST /api/v1/chat-bot/conversation/
Content-Type: application/json
```

**Request Body:**
```json
{
  "action": "summarizer",
  "documentUrl": "https://example.com/document.pdf",
  "minPage": 1,
  "maxPage": 5
}
```

**Response:**
```json
{
  "data": "Summary of the document...",
  "message": "Document summarized successfully"
}
```

#### 4. Question Generation
```http
POST /api/v1/chat-bot/conversation/
Content-Type: application/json
```

**Request Body:**
```json
{
  "action": "generate_questions",
  "documentUrl": "https://example.com/document.pdf",
  "minPage": 1,
  "maxPage": 5
}
```

**Response:**
```json
{
  "data": [
    "Question 1?",
    "Question 2?",
    ...
  ],
  "message": "Questions generated successfully"
}
```

#### 5. Get Options
```http
POST /api/v1/chat-bot/options/
Content-Type: application/json
```

**Request Body:**
```json
{
  "startedChatbot": true
}
```

**Response:**
```json
{
  "options": [
    "question_answer",
    "summarizer",
    "generate_questions"
  ]
}
```

### Action Types

- `question_answer` - Answer questions from PDF content
- `summarizer` - Summarize PDF document
- `generate_questions` - Generate questions from PDF content

### Error Responses

All errors follow this structure:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "Additional error context"
    }
  }
}
```

**Common Error Codes:**
- `VALIDATION_ERROR` - Invalid request data
- `PDF_PROCESSING_ERROR` - PDF processing failed
- `AGENT_ERROR` - AI agent processing error
- `INTERNAL_ERROR` - Server error

---

## Frontend Repository

This backend is designed to work with the File Talk AI frontend:

**Frontend Repository:** [File Talk AI - Frontend (React + Vite)](https://github.com/AkshayPanchivala/filetalkai)

Make sure to configure the frontend's `VITE_API_BASE_URL` environment variable to point to this backend:

```env
VITE_API_BASE_URL=http://localhost:8000
```

---

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Superuser
```bash
python manage.py createsuperuser
```

### Accessing Admin Panel
Navigate to `http://localhost:8000/admin/` after creating a superuser.

---

## Production Deployment

For production deployment:

1. Set `ENVIRONMENT=production` in `.env`
2. Set `DEBUG=False`
3. Configure PostgreSQL database
4. Use Gunicorn as WSGI server
5. Configure static file serving with WhiteNoise
6. Set up proper CORS settings
7. Enable rate limiting and monitoring
8. Consider using Redis for caching

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

- [Django](https://www.djangoproject.com/) - Web framework
- [Django REST Framework](https://www.django-rest-framework.org/) - API toolkit
- [GROQ](https://groq.com/) - LLM inference platform
- [Phidata](https://github.com/phidatahq/phidata) - AI agent framework
- [PyMuPDF](https://pymupdf.readthedocs.io/) - PDF processing library

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## Support

For issues and questions, please open an issue on the [GitHub repository](https://github.com/AkshayPanchivala/File-Talk-AI-Backend/issues).

---

**Built with ❤️ by Akshay Panchivala**