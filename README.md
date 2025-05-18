
# 🧠 File Talk AI – Backend (Django)

This is the backend for **File Talk AI**, a web application that allows users to upload PDF files and interact with them through advanced AI features like question answering, summarization, and question generation using GROQ's LLM.

---

## 🔗 Frontend Repo

👉 [File Talk AI – Frontend (React + Vite)](https://github.com/AkshayPanchivala/filetalkai)

---

## 🚀 Features

- Process PDF files and extract content
- Generate answers from user questions
- Summarize PDF documents
- Generate 20 relevant questions from a document
- Uses **GROQ LLM** for natural language understanding

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/AkshayPanchivala/File-Talk-AI-Backend.git
cd file-talk-ai
````

### 2. Create Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root of your project and add the following variables:

```env
GROQ_API_KEY=your-groq-api-key

```

> ⚠️ Replace `your-groq-api-key` with your actual key from GROQ (see below for how to get it).

---

## 🤖 How to Get GROQ API Key

1. Go to [GROQ Cloud Console](https://console.groq.com/)
2. Sign up or log in
3. Navigate to the **API Keys** section
4. Generate a new API key
5. Copy the key and paste it into your `.env` file as shown above

---

## 🔧 Run the Django Server

Make migrations and run the server:

```bash
python manage.py migrate
python manage.py runserver
```

Backend should now be running at:
👉 `http://localhost:8000`

Make sure your frontend `.env` has the correct `VITE_API_BASE_URL` pointing to this.


---

## 📃 License

This project is licensed under the MIT License.

---

## 🙌 Acknowledgements

* [Django](https://www.djangoproject.com/)
* [GROQ](https://groq.com/)
* [PyMuPDF](https://pymupdf.readthedocs.io/) (for PDF processing)
