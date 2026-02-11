AllyAI
Multi-Agent Anti-Bullying Support System

AllyAI is a real-time, empathetic AI companion designed to detect bullying, harassment, and emotional distress in user conversations. Unlike traditional text-in, text-out chatbots, AllyAI uses a multi-agent architecture that separates emotional analysis from response generation, enabling safer, more nuanced, and analytically rich interactions.

Project Overview

The purpose of AllyAI is to move beyond basic chatbot behavior and build a system that understands emotional context and risk in real time.

Core Goals

Safety first
Prioritize crisis detection and immediate access to human support resources.

Empathetic engagement
Validate user emotions rather than simply offering solutions.

Real-time analytics
Visualize the emotional trajectory of conversations to generate insight.

System Architecture

Multi-Agent Design

AllyAI uses a modular agent-based architecture. The main application (app.py) acts as an orchestrator, coordinating three specialized agents.

Detection Agent

agents/detection_agent.py

Role
The system’s observer. It never speaks directly to the user.

Function
Analyzes every user message before a response is generated.

Outputs

Sentiment: Positive, Neutral, or Negative

Risk level: Low, Medium, High, or Crisis

Emotions: Sadness, Fear, Hope, Anger, etc.

Topics: School, Appearance, Social Pressure, Identity, etc.

Response Agent

agents/response_agent.py

Role
The system’s voice.

Function
Uses the Detection Agent’s analysis to generate an appropriate response persona.

Decision Logic

Low risk
Friendly, conversational support

High risk or bullying detected
Protective persona that validates feelings and encourages trusted adults

Crisis detected
Hard override
AI generation is stopped and a predefined safety response with hotline resources is returned immediately

Analytics Agent

agents/analytics_agent.py

Role
The system’s recorder.

Function
Aggregates emotional and risk metadata without storing private conversation content.

Output
Powers the real-time Empathy Dashboard in the UI, displaying trends across the session.

Technology Stack

Frontend
Streamlit (Python-based interactive UI)

AI Core
Google Gemini using gemini-flash-latest

Visualization
Plotly for interactive emotion and risk charts

Language
Python 3.10 or newer

Architecture
Modular multi-agent pattern

Setup and Usage
Installation

Clone the repository and install dependencies.
pip install -r requirements.txt

Configuration

Create a .env file in the root directory and add your Gemini API key.

GEMINI_API_KEY=your_actual_key_here


A free API key can be generated from Google AI Studio.

Running the Application

Windows
Double-click run_app.bat

Manual

python -m streamlit run app.py

Limitations

This project is a functional prototype and includes the following constraints.

Stateless LLM calls
To reduce token usage, only recent messages are passed to the model. Long-term context may be lost.

No session persistence
The analytics dashboard resets on page refresh. A production system would use a database.

Model misinterpretation
Sarcasm and subtle emotional cues may occasionally be misread.

Rate limits
The free Gemini tier enforces strict quotas. When exceeded, the system switches to an offline fallback mode.

Future Improvements

Planned enhancements for a production-ready version include:

User accounts and persistent history
Store conversations and analytics using a SQL or NoSQL database.

Voice interaction
Add speech-to-text and text-to-speech for hands-free communication.

Intelligent resource recommendations
Suggest location-specific counselors and support groups using geolocation.

Model fine-tuning
Train a smaller open-source model, such as Llama 3, on therapeutic dialogue to improve privacy and reduce external API reliance.

Ethical Considerations

Building AI for mental and emotional support requires strong ethical safeguards.

Non-medical disclaimer
The interface clearly states that AllyAI is not a replacement for professional help.

Crisis interception
Code-level overrides prevent the AI from attempting to manage suicidal ideation. Human professionals are prioritized immediately.

Privacy first
No data is stored permanently. All session data exists only in memory and is erased when the session ends.

Created by David Achinivu
Portfolio Demonstration Project
