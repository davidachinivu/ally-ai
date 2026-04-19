# 🛡️ AllyAI: Multi-Agent Anti-Bullying Support System

**Live Demo:** [https://ally-ai-chat.streamlit.app/](https://ally-ai-chat.streamlit.app/)

**AllyAI** is a real-time, empathetic AI companion designed to detect bullying, harassment, and emotional distress in user conversations. Unlike traditional text-in, text-out chatbots, AllyAI uses a **multi-agent architecture** that separates emotional analysis from response generation, enabling safer, more nuanced, and analytically rich interactions.

---

## 🚀 Project Overview

The purpose of AllyAI is to move beyond basic chatbot behavior and build a system that understands emotional context and risk in real time.

**Core Goals:**
1. **Safety First:** Prioritize crisis detection and immediate access to human support resources.
2. **Empathetic Engagement:** Validate user emotions rather than simply offering solutions.
3. **Real-Time Analytics:** Visualize the emotional trajectory of conversations to generate insight.

---

## 🏗️ System Architecture (Multi-Agent Design)

AllyAI uses a modular agent-based architecture. The main application (`app.py`) acts as an **orchestrator**, coordinating three specialized agents:

### 1. 🕵️ Detection Agent (`agents/detection_agent.py`)
- **Role:** The system’s observer. It never speaks directly to the user.
- **Function:** Analyzes every user message before a response is generated.
- **Outputs:**
  - **Sentiment:** Positive, Neutral, or Negative
  - **Risk level:** Low, Medium, High, or Crisis
  - **Emotions:** Sadness, Fear, Hope, Anger, etc.
  - **Topics:** School, Appearance, Social Pressure, Identity, etc.

### 2. 🗣️ Response Agent (`agents/response_agent.py`)
- **Role:** The system’s voice.
- **Function:** Uses the Detection Agent’s analysis to generate an appropriate response persona.
- **Decision Logic:**
  - *Low risk:* Friendly, conversational support.
  - *High risk or bullying detected:* Protective persona that validates feelings and encourages reaching out to trusted adults.
  - *Crisis detected (Hard Override):* AI generation is stopped, and a predefined safety response with human hotline resources is returned immediately.

### 3. 📊 Analytics Agent (`agents/analytics_agent.py`)
- **Role:** The system’s recorder.
- **Function:** Aggregates emotional and risk metadata without storing private conversation content.
- **Output:** Powers the real-time **Empathy Dashboard** in the UI, displaying trends across the session.

---

## 🛠️ Technology Stack

- **Frontend:** Streamlit (Python-based interactive UI)
- **AI Core:** Google Gemini (`gemini-flash-latest`) via `google-generativeai`
- **Visualization:** Plotly (Interactive emotion and risk charts)
- **Language:** Python 3.10+
- **Architecture:** Modular multi-agent pattern

---

## 💻 Setup and Usage

### 1. Installation
Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the root directory and add your Gemini API key:
```ini
GEMINI_API_KEY=your_actual_key_here
```
*(A free API key can be generated from Google AI Studio.)*

### 3. Running the Application
**Windows (Fastest):**  
Double-click `run_app.bat`

**Manual Form CLI:**  
```bash
python -m streamlit run app.py
```

---

## ⚠️ Limitations

This project is a functional prototype and includes the following constraints:

- **Stateless LLM Calls:** To reduce token usage, only recent messages are passed to the model. Long-term context may be lost.
- **No Session Persistence:** The analytics dashboard resets on page refresh. A production system would use a database.
- **Model Misinterpretation:** Sarcasm and subtle emotional cues may occasionally be misread by the AI.
- **Rate Limits:** The free Gemini tier enforces strict quotas. When exceeded, the system safely switches to an offline fallback mode.

---

## 🔮 Future Improvements

Planned enhancements for a production-ready version include:

- **User Accounts and Persistent History:** Store conversations and analytics using a SQL or NoSQL database.
- **Voice Interaction:** Add speech-to-text and text-to-speech capabilities for hands-free communication.
- **Intelligent Resource Recommendations:** Suggest location-specific counselors and support groups using geolocation.
- **Model Fine-Tuning:** Train a smaller, open-source model (such as Llama 3) specifically on therapeutic dialogue to improve privacy and reduce reliance on external APIs.

---

## ⚖️ Ethical Considerations

Building AI for mental and emotional support requires strong ethical safeguards:

- **Non-Medical Disclaimer:** The interface clearly states that AllyAI is *not* a replacement for professional medical or psychological help.
- **Crisis Interception:** Code-level overrides prevent the AI from attempting to manage suicidal ideation or extreme crisis scenarios. Human professionals and hotlines are prioritized immediately.
- **Privacy First:** No personal data is stored permanently. All session data exists only in memory and is erased when the session ends.

---

*Created by David Achinivu — Portfolio Demonstration Project*
