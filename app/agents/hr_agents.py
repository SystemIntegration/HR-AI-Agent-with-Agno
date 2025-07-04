from agno.agent import Agent
from app.app_generalize_settings import MODEL, GEMINI_API_KEY
from textwrap import dedent
from app.tools.hr_tools import (
    send_policy_request_to_hr,
)
from app.configurations.agents_memory_storage import memory
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from app.services.document_loader_service import DocumentLoader
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.embedder.google import GeminiEmbedder
# Initialize agents

# --- Policy Creation Agent ######################################
policy_creation_agent = Agent(
    name="policy_creation_agent",
    model=MODEL,
    instructions=dedent(
        f"""\

You help when no matching HR policy exists for a user's question.

Steps:
1. Categorize the question:
   - If it fits an existing category → set mode = `update`
   - If not → define a new category → set mode = `create`

2. Generate:
   - A short policy title
   - Clear policy content (use bullet points if needed)

3. Act:
   - If the same `query + category` was already sent → skip and inform user
   - Else → call `send_policy_request_to_hr` with:
       - user_query
       - suggested_policy_content
       - category
       - mode (`update` or `create`)

4. Save memory of this query + category to prevent duplicates

Rules:
- Always act — don’t ask the user
- Don’t mention tools or memory
- End by confirming HR was notified, with action type (new or updated)

        """
    ),
    tools=[send_policy_request_to_hr],
    show_tool_calls=True,
    markdown=True,
    # Memory Config
    memory=memory,
    read_chat_history=True,
    enable_agentic_memory=True,
    # If True, the agent creates/updates user memories at the end of runs
    enable_user_memories=True,
    user_id="default",
    # session_id="fixed_session_id",
    add_history_to_messages=True,
    num_history_runs=3,
)

# --- Policy Agent ######################################


# Load Agno documentation in a knowledge base
pdf_knowledge_base = PDFUrlKnowledgeBase(
    urls=DocumentLoader()._load_documents(),
    num_documents=10,
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="policy_docs",
        search_type=SearchType.hybrid,
        # Use GEMINI for embeddings
        embedder=GeminiEmbedder(id="embedding-001",api_key=GEMINI_API_KEY),
        api_key=GEMINI_API_KEY,
    ),
)

policy_agent = Agent(
    knowledge=pdf_knowledge_base,
    search_knowledge=True,
    name="policy_agent",
    model=MODEL,
    team=[policy_creation_agent],
    instructions=[
        """
    You are a company policy assistant. Answer questions using only the content from company policy documents.

    Follow this process:
        Search the documents for a relevant answer.
        If found, respond with the exact information from the documents.

    If no relevant policy is found:
        Do not guess or generate an answer.
        Call policy_creation_agent.

    Rules to follow:
        Never ask follow-up questions.
        Keep answers brief, factual, and professional.
        Do not use outside knowledge or assumptions.
        
    Reminder: All responses must be grounded in the provided documents. If nothing relevant is found, trigger the fallback process.

        """
    ],
    # Memory Config
    memory=memory,
    read_chat_history=True,
    enable_agentic_memory=True,
    # If True, the agent creates/updates user memories at the end of runs
    enable_user_memories=True,
    user_id="default",
    # session_id="fixed_session_id",
    add_history_to_messages=True,
    num_history_runs=3,
)

policy_agent.knowledge.load(recreate=False,skip_existing=True)