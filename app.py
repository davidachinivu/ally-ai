import streamlit as st
import plotly.express as px
from config import Config
from llm_client import LLMClient
from agents.detection_agent import DetectionAgent
from agents.response_agent import ResponseAgent
from agents.analytics_agent import AnalyticsAgent
import utils

# Page Configuration
st.set_page_config(
    page_title=f"{Config.APP_NAME} - Anti-Bullying Support",
    page_icon="🛡️",
    layout="wide"
)

# --- Initialization ---
if "llm_client" not in st.session_state:
    st.session_state.llm_client = LLMClient()

if "agents" not in st.session_state:
    st.session_state.agents = {
        "detection": DetectionAgent(st.session_state.llm_client),
        "response": ResponseAgent(st.session_state.llm_client),
        "analytics": AnalyticsAgent()
    }

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello. I'm Ally, here to support you. I'm listening."}
    ]

# --- Sidebar ---
with st.sidebar:
    st.title(f"🛡️ {Config.APP_NAME}")
    st.caption(f"v{Config.VERSION}")
    
    st.markdown("### System Status")
    if st.session_state.llm_client.provider == "offline":
        st.warning("🔴 Offline Mode (Mock)")
        st.info("Add `GEMINI_API_KEY` to .env to go online.")
    else:
        st.success(f"🟢 Online ({st.session_state.llm_client.provider.upper()})")
        
    st.markdown("---")
    st.markdown(utils.get_sidebar_content())
    
    if st.button("Clear Conversation"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Conversation cleared. How can I help?"}
        ]
        st.session_state.agents["analytics"].session_data = [] # Clear analytics too
        st.rerun()

# --- Main Interface ---
tab1, tab2 = st.tabs(["💬 Chat", "📊 Analytics Dashboard"])

with tab1:
    st.title("AllyAI: Supportive Chat Companion")
    
    # Display Chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "analysis" in msg:
                # Debug expander to show internals (Portfolio Feature!)
                with st.expander("🔍 System Analysis (For Debug)"):
                    st.json(msg["analysis"])

    # User Input
    if prompt := st.chat_input("Type your message here..."):
        # 1. User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Agent Orchestration
        with st.chat_message("assistant"):
            with st.spinner("Analyzing & Thinking..."):
                # Step A: Detection Agent
                analysis = st.session_state.agents["detection"].process(prompt)
                
                # Step B: Analytics Agent (Log data)
                st.session_state.agents["analytics"].log_interaction(prompt, analysis)
                
                # Step C: Response Agent
                response_text = st.session_state.agents["response"].process(prompt, analysis)
                
                st.markdown(response_text)
                
                # Show Analysis immediately for portfolio demo purposes
                with st.expander("🔍 System Analysis (For Debug)"):
                    st.json(analysis)

        # 3. Add to History
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response_text,
            "analysis": analysis
        })

with tab2:
    st.title("Real-Time Empathy Dashboard")
    st.markdown("This dashboard visualizes the emotional journey of the conversation in real-time.")
    
    df = st.session_state.agents["analytics"].get_dataframe()
    
    if not df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Risk Levels")
            fig_risk = px.histogram(df, x="risk_level", title="Risk Level Distribution", color="risk_level")
            st.plotly_chart(fig_risk, use_container_width=True)
            
        with col2:
            st.subheader("Detected Emotions")
            fig_emotion = px.bar(df, x="primary_emotion", title="Emotional Tone", color="primary_emotion")
            st.plotly_chart(fig_emotion, use_container_width=True)
            
        st.subheader("Session Data log")
        st.dataframe(df)
    else:
        st.info("Start chatting to see analytics data appeared here!")
