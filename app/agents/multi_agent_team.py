from app.agents.hr_agents import policy_agent,policy_creation_agent
from agno.team.team import Team
from app.configurations.agents_memory_storage import memory,agent_storage
from app.app_generalize_settings import MODEL

# --- Multi-Agent Team ---
multi_agent_team = Team(
    members=[policy_agent,policy_creation_agent],
    mode="coordinate",
    model=MODEL,
    name="Multi Agent Team",
instructions=[
    """
You are a team that answers employee questions using company policy documents.

Rules:
1. Always send the question to `policy_agent` to search the knowledge base.
2. If `policy_agent` cannot find an answer → it must trigger `policy_creation_agent` to notify HR.

Goal:
- Always answer using the knowledge base (policy documents).
- If no match and question is related to company policy, ensure `policy_creation_agent` notifies HR to create or update the policy.
- Other than company policy question, provide response that don't have experties.

Guidelines:
- Do not ask the user whether to notify HR — always take the necessary action automatically.
- Do not ask follow-up questions — proceed with the appropriate action immediately.
- Maintain a clear and professional tone.
- Do not mention internal tools, agents, or memory operations to the user.
- Always end by confirming that HR has been notified, specifying whether it was for a **new** or **updated** policy.
- Always check memory before acting: if an email has already been sent for the same user query and category, do not repeat the process and respond accordingly.
- Focus on helping the user efficiently without drawing attention to internal errors or system limitations.
- Responses should be professional, concise, and user-focused.


    """
],

    markdown=True,
    show_tool_calls=True,
    ## Memory config
    memory=memory,
    enable_agentic_memory=True,
    enable_user_memories=True,
    enable_team_history=True,
    num_history_runs = 3,
    storage=agent_storage,
    user_id='default',
    # session_id='fixed_session_id',
    team_id='default',


)