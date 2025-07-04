from agno.memory.v2.memory import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.storage.sqlite import SqliteStorage


# --- Setup Persistent Memory and Storage ---
memory = Memory(
    db=SqliteMemoryDb(
        table_name="memories",
        db_file="tmp/memory.db"
    )
)

agent_storage = SqliteStorage(
    table_name="agent_sessions",
    db_file="tmp/agent_storage.db",
    auto_upgrade_schema=True,
    mode='team'
)