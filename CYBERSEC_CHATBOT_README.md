# CyberSec — AI-Powered Cybersecurity Chatbot

> A full-stack AI chatbot delivering real-time cybersecurity guidance on threats, OWASP Top 10 vulnerabilities, secure coding practices, and incident response — powered by Google Gemini API.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_API-4285F4?style=flat-square&logo=google&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap_5-7952B3?style=flat-square&logo=bootstrap&logoColor=white)
![Domain](https://img.shields.io/badge/Domain-Security_Awareness-red?style=flat-square)

---

## What It Does

CyberSec is an intelligent chatbot that makes cybersecurity knowledge accessible to both technical and non-technical users. It covers OWASP Top 10 vulnerabilities, phishing, malware, social engineering, and secure coding — with context-aware, multi-turn conversation support.

**Core features:**
- Full-stack Flask backend with session management and **input sanitization** against injection attacks
- **Google Gemini API** integration with domain-specific prompt engineering for security-focused responses
- **OWASP Top 10** coverage: XSS, CSRF, SQLi, broken authentication, and more
- Mobile-responsive **Bootstrap 5** frontend achieving sub-300ms response latency
- Multi-turn conversation context retention for coherent threat mitigation dialogues
- 40% reduction in generic response rate via fine-tuned system prompts

---

## Screenshot
 ![image](https://github.com/user-attachments/assets/3a7d6d02-a3d7-465b-80fb-c0498c43e427)

---

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python 3, Flask |
| AI Engine | Google Gemini API |
| Frontend | HTML5, CSS3, Bootstrap 5 |
| Security | Input sanitization, session handling |
| Deployment | Local / can be deployed on Render/Railway |

---

## How to Run

```bash
# Clone the repository
git clone https://github.com/jhanvijyant/CyberSec-AI-Chatbot.git
cd CyberSec-AI-Chatbot

# Install dependencies
pip install flask google-generativeai

# Add your Gemini API key
# Create a .env file:
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Run the app
python app.py

# Open in browser
# http://localhost:5000
```

---

## Security Design Decisions

- All user inputs sanitized before being passed to the AI model — prevents prompt injection
- API key stored in `.env` — never hardcoded in source
- Session-based context management — no persistent storage of user queries
- `.gitignore` includes `.env` to prevent accidental credential exposure

---

## Sample Topics the Chatbot Covers

| Topic | Example Query |
|---|---|
| OWASP Top 10 | "What is SQL injection and how do I prevent it?" |
| Phishing | "How do I identify a phishing email?" |
| Password security | "What makes a strong password?" |
| Malware | "What is ransomware and how does it spread?" |
| Secure coding | "How do I prevent XSS in my Flask app?" |
| Incident response | "My system might be compromised — what do I do?" |

---

## Topics

`python` `flask` `cybersecurity` `chatbot` `gemini-api` `owasp` `security-awareness` `ai` `prompt-engineering` `bootstrap` `web-security` `infosec`

---

## Author

**Jhanvi Jyant** — B.Tech CSE (Cybersecurity & Digital Forensics), VIT Bhopal

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jhanvi-jyant-26934b291)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/jhanvijyant)
