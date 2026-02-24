# ⚖️ AI Lawyer Chatbot with Automated Email Reporting

## 📌 Overview

AI Lawyer Chatbot is a Flask-based web application that delivers professional legal assistance strictly limited to Indian law. The system uses the Groq LLM (LLaMA 3.3 70B) to generate structured legal responses and automatically emails chat logs when the session ends.

The application ensures:
- Responses are strictly law-related
- Indian jurisdiction is followed
- Legal citations (Acts, Sections, Articles) are included
- A formal professional tone is maintained
- Non-legal queries are refused
- Chat logs are automatically emailed when the user types **"bye"**
- AI responses are converted into speech

---

## 🚀 Features

- 🧠 AI-powered legal assistant (Groq – LLaMA 3.3 70B)
- 🇮🇳 Focused on Indian legal jurisdiction
- 📜 Structured legal answer format
- 📝 Automatic chat logging
- 📧 Email report generation using MailerSend
- 🔊 Text-to-Speech integration (pyttsx3)
- 🔒 Restriction to law-related questions only

---

## 🏗️ Tech Stack

| Technology | Purpose |
|------------|----------|
| Flask | Backend web framework |
| Groq API | Large Language Model (LLM) |
| MailerSend | Email delivery service |
| pyttsx3 | Text-to-Speech engine |
| Python Logging | Chat history logging |

---

## ⚙️ Application Workflow

### 1️⃣ User Sends Query
The frontend sends a POST request to:

```
/chat
```

### 2️⃣ AI Processing
- A strict system prompt defines:
  - Indian jurisdiction
  - Mandatory legal citation
  - Formal tone
  - Refusal of non-legal queries
- Groq generates a structured legal response.

### 3️⃣ Chat Logging
All user messages and AI responses are stored in:

```
logs/AI_lawyer_chat.log
```

### 4️⃣ Email Report Trigger
When the user types:

```
bye
```

The system:
- Reads the log file
- Builds an email containing the full conversation
- Sends it using the MailerSend API
- Logs any email errors if they occur

### 5️⃣ Text-to-Speech Output
The AI response is spoken aloud using `pyttsx3`.

---

## 📂 Project Structure

```
AI-Lawyer-Chatbot/
│
├── app.py
├── templates/
│   └── index.html
├── logs/
│   └── AI_lawyer_chat.log
├── requirements.txt
└── README.md
```

---

## 🔐 Configuration

```
GROQ_API_KEY=your_groq_api_key
MAILERSEND_API_KEY=your_mailersend_api_key
```

Then access them in Python:

```python
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
ms = MailerSendClient(api_key=os.getenv("MAILERSEND_API_KEY"))
```

---

## 📑 AI Response Format

Every legal response follows this structure:

1. Brief Legal Summary  
2. Relevant Law Citation(s)  
3. Explanation  
4. Practical Legal Steps (if applicable)  
5. Short and precise reply  

---

## ⚠️ Important Notes

- This system is for informational legal assistance only.
- It does not replace a licensed advocate.
- Always verify legal advice with a qualified legal professional.
- Ensure API keys are secured before deploying publicly.

---

## 📧 Automated Email Report

When the user ends the conversation with **"bye"**, the complete chat history is emailed to the configured recipient automatically.

---
