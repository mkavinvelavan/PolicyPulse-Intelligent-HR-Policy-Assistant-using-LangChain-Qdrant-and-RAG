# ui/app.py
import streamlit as st
import requests
import time
import textwrap

API_URL = "http://localhost:8000/ask"
VIEW_MEMORY = "http://localhost:8000/memory/view"
CLEAR_MEMORY = "http://localhost:8000/memory/clear"

st.set_page_config(page_title="PolicyPulse", page_icon="📘")
st.title("📘 PolicyPulse — HR Policy Assistant")

st.markdown("""
### 👋 Welcome to PolicyPulse — Your HR Policy Assistant

You can ask me anything related to your company's HR policies, including:

#### ✅ Available Policy Categories
- 🟦 Leave & Attendance Policies  
- 🟩 Work From Home / Hybrid Guidelines  
- 🟨 Reimbursement & Expense Policies  
- 🟪 Code of Conduct & Ethics  
- 🟥 IT & Security Policies  
- 🟧 Travel Policies  
- 🟫 Workplace Behavior & Safety  

#### 💡 Examples of Questions You Can Ask
- *"How many casual leaves are allowed?"*  
- *"What is the work-from-home policy?"*  
- *"Explain the reimbursement process."*  
- *"What is the notice period after resignation?"*  
- *"Tell me about the dress code policy."*

#### 📁 Policies Loaded Into the System
I currently have access to **your company’s 14 official HR policy PDFs**, and I only answer based on those documents.

---

Feel free to ask anything! I'm here to guide you. 🙂
""")


# --- User identity ---
if "user_id" not in st.session_state:
    st.session_state.user_id = st.text_input(
        "Enter your name (used for session memory)",
        value="employee",
        key="user_input"
    )

if not st.session_state.user_id:
    st.session_state.user_id = "employee"


# --- Memory Buttons ---
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("View Memory"):
        try:
            r = requests.post(VIEW_MEMORY, json={"user": st.session_state.user_id})
            mem = r.json().get("memory", [])
            st.write("Session memory (most recent):")
            st.json(mem)
        except Exception as e:
            st.error(f"Could not fetch memory: {e}")

with col2:
    if st.button("Clear Memory"):
        try:
            r = requests.post(CLEAR_MEMORY, json={"user": st.session_state.user_id})
            st.success("Memory cleared.")
        except Exception as e:
            st.error(f"Could not clear memory: {e}")


# --- Init messages list ---
if "messages" not in st.session_state:
    st.session_state.messages = []


# --- Chat Input ---
user_input = st.chat_input("Ask anything about company policies (leave, WFH, expenses...)")

if user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Send to backend
    payload = {"user": st.session_state.user_id, "question": user_input}

    try:
        r = requests.post(API_URL, json=payload, timeout=30)
    except Exception as e:
        st.error(f"API error: {e}")
        raise

    # Validate Response
    if r.status_code != 200:
        st.error(f"Server error {r.status_code}: {r.text}")
    else:
        data = r.json()
        answer = data.get("answer", "")
        sources = data.get("sources", [])

        # Assistant bubble (formatted markdown)
        with st.chat_message("assistant"):
            st.markdown(answer, unsafe_allow_html=True)

        # Save in history
        st.session_state.messages.append({"role": "assistant", "content": answer})

        # Show retrieved docs
        if sources:
            with st.expander("📄 Sources / Retrieved docs"):
                st.write(sources)


# --- Conversation History (inside dropdown) ---
with st.expander("📜 Conversation History (Click to expand)"):
    if st.session_state.messages:
        for msg in st.session_state.messages[-20:]:
            role = msg["role"]
            if role == "user":
                st.markdown(f"**🧑 You:** {msg['content']}")
            else:
                st.markdown(f"**🤖 PolicyPulse:** {msg['content']}")
