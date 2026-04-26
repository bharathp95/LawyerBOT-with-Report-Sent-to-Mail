from flask import Flask, render_template, request, jsonify
import logging
from groq import Groq
from mailersend import MailerSendClient, EmailBuilder
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# ===============================
# Create Logger
# ===============================


log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)
log.propagate = False

# Disable httpx info logs
logging.getLogger("httpx").setLevel(logging.WARNING)

# ===============================
# Initialize Groq Client
# ===============================
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

ms = MailerSendClient(api_key=os.getenv("MAILERSEND_API_KEY"))



# ===============================
# Route: Home Page
# ===============================
@app.route("/")
def home():
    return render_template("index.html")

# ===============================
# Route: Chat API
# ===============================
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json["message"]

        # Log user message
        logging.info(f"User: {user_message}")

        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """ You are a professional legal lawyer AI assistant.

            Your role:
            - You ONLY answer questions related to law, legal rights, legal procedures, legal documents, regulations, compliance, and court processes.
            - If a question is not related to law, you must politely refuse and state that you only answer law-related questions.
            - You must always respond in a formal, professional legal tone.
            - You must always cite the applicable law, statute, regulation, constitutional article, or legal principle when giving an answer.
            - When possible, mention:
            - The exact Act or Code name
            - Relevant section or article number
            - Jurisdiction is Indian 
            - Do not provide casual opinions.
            - Do not answer general knowledge, medical, technical, entertainment, or personal advice questions.

            Answer format:
            1. Brief legal summary
            2. Relevant law citation(s)
            3. Explanation
            4. Practical legal steps (if applicable)
            5. keep a short reply
            6. when user says bye, greet goodbye """
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        reply = chat_completion.choices[0].message.content.strip()

        # Log AI response
        logging.info(f"\nAI: {reply} \n")

        # ===============================
        # If user says bye → Send Logs
        # ===============================
        if user_message.lower().strip() == "bye":
            try:
                with open("logs/AI_lawyer_chat.log", "r") as file:
                    log_content = file.read()

                email = (
                    EmailBuilder()
                    .from_email("info@", "AI Lawyer")
                    .to_many([{"email": "bharath.98458@gmail.com", "name": "Recipient"}])
                    .subject("AI Lawyer Chat Logs")
                    .html(f"<pre>{log_content}</pre>")
                    .text(log_content)
                    .build()
                )

                ms.emails.send(email)
                ms.emails.send(email)

                # clear log file
                open("logs/AI_lawyer_chat.log", "w").close()

            except Exception as mail_error:
                logging.error(f"Email Error: {str(mail_error)}")

        return jsonify({"reply": reply})

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"reply": "An error occurred."}), 500

# ===============================
# Run App
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
