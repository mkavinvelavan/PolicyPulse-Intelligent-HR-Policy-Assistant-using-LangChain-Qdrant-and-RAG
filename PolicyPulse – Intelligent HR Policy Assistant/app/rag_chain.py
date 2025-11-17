# app/rag_chain.py
import os
from dotenv import load_dotenv
from groq import Groq
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

# Config
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "policypulse_policies"
GROQ_MODEL = "llama-3.1-8b-instant"  # working model

# Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

# Embeddings & vectorstore
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
qdrant_client = QdrantClient(url=QDRANT_URL)
vectorstore = Qdrant(client=qdrant_client, collection_name=COLLECTION_NAME, embeddings=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# In-memory conversation memory store (simple). Keys = user ids, value = list of {"role","content"}.
# Note: this is ephemeral (process memory). For production, use Redis or a DB.
CONVERSATION_MEMORY = {}
MEMORY_LIMIT = 10  # number of previous messages to keep (user+assistant pairs)

def add_to_memory(user_id: str, role: str, content: str):
    mem = CONVERSATION_MEMORY.setdefault(user_id, [])
    mem.append({"role": role, "content": content})
    # Trim to last MEMORY_LIMIT messages
    if len(mem) > MEMORY_LIMIT:
        # keep last MEMORY_LIMIT items
        CONVERSATION_MEMORY[user_id] = mem[-MEMORY_LIMIT:]

def get_memory(user_id: str):
    return CONVERSATION_MEMORY.get(user_id, [])

def clear_memory(user_id: str):
    CONVERSATION_MEMORY[user_id] = []

def assemble_prompt(context: str, memory: list, question: str) -> list:
    """
    Build messages list for Groq chat API:
    - system message (instructions + context)
    - memory messages (alternating user/assistant)
    - current user question
    """
    system_prompt = f"""
You are **PolicyPulse**, a professional HR policy assistant.

Your responsibilities:
- Answer ONLY using the information found in the provided context.
- Keep responses natural, readable, and human-like.
- Do NOT invent or assume any policy details not found in the context.

================== RESPONSE STYLE RULES ==================

### 1️⃣ Natural Explanation
- Use a clear paragraph when describing what a policy means.
- No forced sections, no fixed templates.

### 2️⃣ Bullet Points Only When Needed
Use bullet points ONLY for:
- rules
- eligibility criteria
- do/don’t lists
- important notes
- steps or procedures
(Use bullets only when they improve clarity.)

### 3️⃣ Short vs Long Answers
If the user says:
- "short"
- "brief"
- "in short"
- "quick summary"

→ Provide a very short 3–5 line summary.

If not, give a normal detailed explanation.

### 🟦 Missing Topic Handling (NEW)
If the user asks for “short”, “brief”, or “summary”  
**without specifying a policy/topic** AND  
there is **no previous conversation memory**:

→ Ask: “Sure — which policy would you like a short summary of?”  
→ Do NOT answer randomly.

### 4️⃣ Greeting & Small-Talk Handling
If the user says:
- hi, hello, hey
- thanks, thank you
- who are you, what can you do
- bye, good night

→ Give a short friendly conversational reply (NOT a policy answer).

### 5️⃣ Smart Topic Detection (NEW)
For vague or unclear questions:
- Identify possible matching policy topics from keywords such as:
  - "WFH", "work from home", "remote"
  - "leave", "holiday", "absence"
  - "attendance", "late", "early going"
  - "IT policy", "security", "password"
  - "reimbursement", "expenses", "claims"
  - "travel", "trip", "TA/DA"
  - "code of conduct", "behavior", "ethics"

If multiple topics match → ask a clarification question like:
“Do you mean Work-From-Home, Leave Policy, or Attendance Policy?”

If NO topic matches → ask:
“Which policy are you referring to?”

### 6️⃣ Smarter Feedback (NEW)
If the user asks something broad like:
- “Tell me the rules”
- “Explain the policy”
- “How does this work?”
- “Give details”

And no topic is clearly identified:

→ Politely guide the user:
“Can you tell me which policy you want details about?  
I can help with WFH, Leave, Attendance, Travel, Reimbursement, IT Security, and more.”

### 7️⃣ Hallucination Control
If the context does NOT contain the answer:
Reply:
"This information does not appear in the policy documents. Could you rephrase or add more details?"

Tone: friendly, clear, helpful.

---------------------------------------------------------
📄 CONTEXT:
{context}
"""




    messages = [{"role": "system", "content": system_prompt}]

    # append memory (if any)
    for m in memory:
        # memory items should be small dicts with role and content
        messages.append({"role": m["role"], "content": m["content"]})

    # finally append the user's current question
    messages.append({"role": "user", "content": question})
    return messages

def retrieve_context(query: str) -> str:
    """
    Retrieve most-relevant docs from Qdrant retriever.
    Uses retriever.invoke() which returns a list of Documents.
    """
    try:
        docs = retriever.invoke(query)
    except Exception:
        # fallback to protected internal call if API differs
        docs = retriever._get_relevant_documents(query)
    context = "\n\n".join([d.page_content for d in docs]) if docs else ""
    return context, docs

def generate_answer(user_id: str, question: str):
    """
    Main entrypoint for server: returns (answer_text, sources:list)
    - uses memory for conversation history
    - stores question+answer back into memory
    """
    q = question.strip()
    # 🌟 1. GREETING HANDLER
    greetings = ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]
    if any(g == q or g in q for g in greetings):
        greeting = (
            "Hello! 👋 I'm PolicyPulse — your HR policy assistant.\n\n"
            "You can ask me about leave, attendance, WFH, reimbursements, code of conduct, and other HR policies."
        )
        add_to_memory(user_id, "user", question)
        add_to_memory(user_id, "assistant", greeting)
        return greeting, []

    # 🌟 2. GRATITUDE HANDLER
    gratitude = ["thanks", "thank you", "thank u", "thx", "tnx", "thanks a lot", "thank you so much"]
    if any(g in q for g in gratitude):
        reply = "You're welcome! 😊 Happy to help. If you have more questions, feel free to ask anytime!"
        add_to_memory(user_id, "user", question)
        add_to_memory(user_id, "assistant", reply)
        return reply, []

    # 2) Retrieve context
    context, docs = retrieve_context(question)

    # 3) Smart fallback if empty context
    if not context.strip():
        fallback = (
            "I couldn't locate any related information in the policy documents.\n\n"
            "Try rephrasing your question or specify the policy area (leave, attendance, WFH, conduct, reimbursements, etc.)."
        )
        add_to_memory(user_id, "user", question)
        add_to_memory(user_id, "assistant", fallback)
        return fallback, []

    # 4) Build prompt with memory
    memory = get_memory(user_id)
    messages = assemble_prompt(context, memory, question)

    # 5) Call Groq
    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        max_tokens=500
    )

    # 6) Extract answer (groq returns object)
    answer = response.choices[0].message.content

    # 7) Save QA to memory
    add_to_memory(user_id, "user", question)
    add_to_memory(user_id, "assistant", answer)

    # Prepare sources list (filename metadata)
    sources = []
    for d in docs:
        src = d.metadata.get("source") if hasattr(d, "metadata") else None
        sources.append({"source": src})

    return answer, sources
