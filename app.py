import streamlit as st
import google.generativeai as genai
from memory.session_memory import SessionMemory
from dotenv import load_dotenv
import os

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Career Copilot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background */
.stApp {
    background: #0d0f14;
    color: #e8eaf0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #13161e !important;
    border-right: 1px solid #1e2330;
}

/* Hero header */
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.03em;
    line-height: 1.1;
}

.hero-subtitle {
    font-size: 0.9rem;
    color: #6b7280;
    margin-top: 4px;
    font-weight: 400;
}

/* Accent pill */
.status-pill {
    display: inline-block;
    background: #1a2744;
    color: #60a5fa;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid #2a3f6e;
    margin-bottom: 12px;
}

/* Chat messages */
.user-bubble {
    background: #1a2744;
    border: 1px solid #2a3f6e;
    border-radius: 14px 14px 4px 14px;
    padding: 12px 16px;
    margin: 8px 0;
    color: #e2e8f0;
    font-size: 0.92rem;
    max-width: 80%;
    margin-left: auto;
}

.agent-bubble {
    background: #131820;
    border: 1px solid #1e2330;
    border-radius: 14px 14px 14px 4px;
    padding: 12px 16px;
    margin: 8px 0;
    color: #cbd5e1;
    font-size: 0.92rem;
    max-width: 85%;
}

.agent-label {
    font-size: 0.7rem;
    color: #60a5fa;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 4px;
}

/* Input area */
.stTextInput > div > div > input {
    background: #13161e !important;
    border: 1px solid #1e2330 !important;
    color: #e8eaf0 !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
}

/* Buttons */
.stButton > button {
    background: #2563eb !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 8px 20px !important;
    transition: background 0.2s !important;
}

.stButton > button:hover {
    background: #1d4ed8 !important;
}

/* Divider */
.divider {
    border: none;
    border-top: 1px solid #1e2330;
    margin: 16px 0;
}

/* Sidebar cards */
.memory-card {
    background: #0d0f14;
    border: 1px solid #1e2330;
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 10px;
    font-size: 0.82rem;
    color: #94a3b8;
}

.memory-label {
    font-size: 0.68rem;
    color: #60a5fa;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)


# ── Gemini setup ──────────────────────────────────────────────────────────────
def get_gemini_model():
    api_key = st.session_state.get("api_key", "")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction="""You are Career Copilot — a sharp, concise career advisor for tech professionals.
        
Your job:
- Help users plan their career path in Data Analytics, ML Engineering, and Software Development
- Analyze skills gaps and suggest what to learn next
- Help with resume advice, job search strategy, and interview prep
- Be direct and specific, not generic

Always:
- Give actionable advice, not vague suggestions
- Ask clarifying questions to understand the user's current level and goals
- Remember context from earlier in the conversation
- Keep responses focused and scannable

You're talking to a final-year B.E. student in AI & Data Science who is job hunting.
Start by understanding their specific goals before advising."""
    )


# ── Session state init ─────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "memory" not in st.session_state:
    st.session_state.memory = SessionMemory()
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("GEMINI_API_KEY", "")


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="hero-title" style="font-size:1.2rem;">⚙️ Setup</div>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    api_key_input = st.text_input(
        "Google AI Studio API Key",
        type="password",
        placeholder="AIza...",
        value=st.session_state.api_key
    )
    if api_key_input:
        st.session_state.api_key = api_key_input
        st.session_state.chat_session = None  # reset on key change

    st.markdown("<br>", unsafe_allow_html=True)

    # Memory display
    st.markdown('<div class="memory-label">📋 Session Memory</div>', unsafe_allow_html=True)
    mem = st.session_state.memory
    memory_data = mem.get_all()

    if memory_data:
        for key, value in memory_data.items():
            st.markdown(f"""
            <div class="memory-card">
                <div class="memory-label">{key}</div>
                {value}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="memory-card">Nothing stored yet. Start chatting!</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Day tracker
    st.markdown('<div class="memory-label">📅 Course Progress</div>', unsafe_allow_html=True)
    days = [
        ("Day 1", "Agents & Vibe Coding", True),
        ("Day 2", "Tools & APIs", False),
        ("Day 3", "Memory & Skills", False),
        ("Day 4", "Security & Eval", False),
        ("Day 5", "Production Deploy", False),
    ]
    for day, topic, done in days:
        icon = "✅" if done else "⬜"
        color = "#60a5fa" if done else "#4b5563"
        st.markdown(f'<div style="font-size:0.78rem;color:{color};padding:3px 0;">{icon} <b>{day}</b>: {topic}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat_session = None
        st.session_state.memory = SessionMemory()
        st.rerun()


# ── Main UI ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="status-pill">Day 1 · Agents & Vibe Coding</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Career Copilot 🚀</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Your AI-powered career advisor — built for the Kaggle AI Agents Intensive</div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# API key guard
if not st.session_state.api_key:
    st.markdown("""
    <div style="background:#1a1f2e;border:1px solid #2a3f6e;border-radius:12px;padding:24px;text-align:center;margin-top:40px;">
        <div style="font-size:2rem;margin-bottom:12px;">🔑</div>
        <div style="color:#e2e8f0;font-weight:600;font-size:1rem;">Add your API Key to get started</div>
        <div style="color:#6b7280;font-size:0.85rem;margin-top:6px;">
            Get a free key at <a href="https://aistudio.google.com/apikey" target="_blank" style="color:#60a5fa;">aistudio.google.com</a>
            → then paste it in the sidebar
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Init chat session with Gemini
if st.session_state.chat_session is None:
    model = get_gemini_model()
    if model:
        st.session_state.chat_session = model.start_chat(history=[])

# Welcome message on first load
if not st.session_state.messages:
    st.markdown("""
    <div class="agent-label">Career Copilot</div>
    <div class="agent-bubble">
        Hey! I'm your Career Copilot 👋<br><br>
        I can help you with:
        <ul style="margin:8px 0 0 0;padding-left:18px;color:#94a3b8;">
            <li>Career roadmaps for Data / ML / Backend roles</li>
            <li>Skills gap analysis</li>
            <li>Resume and LinkedIn advice</li>
            <li>Interview preparation</li>
        </ul>
        <br>
        To get started — <b>what role are you targeting right now?</b>
    </div>
    """, unsafe_allow_html=True)

# Render chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="agent-label">Career Copilot</div><div class="agent-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

# ── Chat input ─────────────────────────────────────────────────────────────────
with st.form("chat_form", clear_on_submit=True):
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        user_input = st.text_input(
            "Message",
            placeholder="Ask anything about your career...",
            label_visibility="collapsed"
        )
    with col_btn:
        submitted = st.form_submit_button("Send →")

if submitted and user_input.strip():
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Update memory with simple keyword extraction
    mem = st.session_state.memory
    lower = user_input.lower()
    if any(w in lower for w in ["want to be", "goal is", "targeting", "i want"]):
        mem.update("career_goal", user_input)
    if any(w in lower for w in ["know", "skills", "experience", "worked with", "i use"]):
        mem.update("mentioned_skills", user_input)

        # Call Gemini
    with st.spinner("Thinking..."):
        try:
            # Build context with memory
            context = ""
            if mem.get_all():
                context = f"\n\n[User context so far: {mem.get_all()}]\n\n"

            response = st.session_state.chat_session.send_message(context + user_input)
            reply = response.text

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

        except Exception as e:

            if "429" in str(e):
                reply = "⏳ Gemini rate limit reached. Please wait 30-60 seconds and try again."

            elif "404" in str(e):
                reply = "⚠️ Gemini model not found. Check the model name in app.py."

            elif "quota" in str(e).lower():
                reply = "⚠️ Gemini free-tier quota exceeded. Wait a few minutes and try again."

            else:
                reply = f"⚠️ Error: {str(e)}"

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

    st.rerun()