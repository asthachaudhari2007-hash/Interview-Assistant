# 🎯 AI Interview Preparation Assistant

An AI-powered Interview Preparation Assistant built with **Streamlit**, **LangChain**, **Google Gemini**, and **RAG (Retrieval-Augmented Generation)** to help candidates practice technical interviews, receive AI-powered feedback, and track their progress.

---

## 🚀 Features

- ✅ AI-generated interview questions
- ✅ Multiple interview types
  - Technical Interview
  - HR Interview
  - Behavioral Interview
- ✅ Difficulty Levels
  - Easy
  - Medium
  - Hard
- ✅ AI Evaluation of Answers
- ✅ Personalized Feedback
- ✅ Strengths & Weaknesses Analysis
- ✅ Interview Performance Report
- ✅ Progress Dashboard
- ✅ Interview History
- ✅ PDF Report Generation
- ✅ RAG-based Context Retrieval
- ✅ Google Gemini Integration

---

# 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| Streamlit | User Interface |
| LangChain | LLM Orchestration |
| Google Gemini | Large Language Model |
| FAISS | Vector Database |
| Sentence Transformers | Text Embeddings |
| PyPDF | PDF Processing |
| ReportLab | PDF Report Generation |
| Python Dotenv | Environment Variables |

---

# 📂 Project Structure

```
Interview_Preparation_Assistant/
│
├── agents/
│   ├── question_agent.py
│   ├── evaluation_agent.py
│   ├── feedback_agent.py
│   └── report_agent.py
│
├── rag/
│   ├── pdf_loader.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── retriever.py
│   └── vector_store.py
│
├── pages/
│   ├── dashboard.py
│   └── history.py
│
├── utils/
│   ├── helper.py
│   ├── session.py
│   ├── styles.py
│   └── pdf_generator.py
│
├── uploads/
├── assets/
├── database/
│
├── app.py
├── llm.py
├── prompts.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/Interview_Preparation_Assistant.git
```

Move into the project directory

```bash
cd Interview_Preparation_Assistant
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
```

---

# ▶️ Run the Project

```bash
streamlit run app.py
```

---

# 🧠 How It Works

1. User selects interview type.
2. User enters:
   - Job Role
   - Experience
   - Difficulty Level
3. AI generates interview questions.
4. User answers each question.
5. Gemini evaluates the response.
6. AI provides:
   - Score
   - Strengths
   - Weaknesses
   - Suggestions
7. A final interview report is generated.
8. Dashboard tracks interview history and performance.

---

# 📊 Evaluation Metrics

The AI evaluates candidates on:

- Technical Skills
- Communication Skills
- Problem Solving
- Confidence
- Overall Score
- Areas for Improvement
- Final Recommendation

---

# 🤖 AI Models

Currently Supported

- Google Gemini 2.5 Flash

---

# 📸 Screenshots

## Home Page

_Add screenshot here_

---

## Interview Page

_Add screenshot here_

---

## Dashboard

_Add screenshot here_

---

## Interview Report

_Add screenshot here_

---

# Future Improvements

- 🎤 Voice-based Interview
- 📹 Webcam Interview Analysis
- 😊 Facial Expression Detection
- 🌍 Multi-language Support
- 📈 Analytics Dashboard
- 📱 Mobile Responsive UI
- ☁ Cloud Deployment
- 🔐 User Authentication

---

# Requirements

- Python 3.10+
- Streamlit
- LangChain
- Google Gemini API Key

---

# Author

**Astha Chaudhari**

GitHub: https://github.com/asthachaudhari2007-hash

LinkedIn: *(Add your LinkedIn profile here)*

---

# License

This project is licensed under the MIT License.

---

# ⭐ If you like this project

Please consider giving it a **Star ⭐** on GitHub.