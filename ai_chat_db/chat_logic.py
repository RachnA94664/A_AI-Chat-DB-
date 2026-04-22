import asyncio
from typing import Optional
from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage
from langchain.agents.middleware import before_model
from langchain_core.messages.utils import get_buffer_string
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware


# ==========================================================
# 🧩 1️⃣ LLM Setup
# ==========================================================

def init_llm(model_name: str, provider: str, api_key: str):
    """Initialize the language model dynamically based on provider."""
    provider = provider.lower().strip()

    if provider == "groq":
        # 🧠 Groq LLM (e.g., llama-3.1-8b-instant)
        return ChatGroq(
            model=model_name,
            api_key=api_key,
            temperature=0.2,
            streaming=True,
        )

    elif provider == "openai":
        # 🤖 OpenAI LLM (e.g., gpt-4o-mini, gpt-4-turbo)
        return ChatOpenAI(
            model=model_name,
            api_key=api_key,
            temperature=0.2,
            streaming=True,
        )

    else:
        # 🪶 Fallback to LangChain’s unified model init
        print(f"⚠️ Unknown provider '{provider}', using default init_chat_model()")
        return init_chat_model(
            model_name,
            model_provider=provider,
            api_key=api_key,
            temperature=0.2
        )

# ==========================================================
# 🗄️ 2️⃣ Database Setup
# ==========================================================
def init_database(db_uri: str) -> SQLDatabase:
    """Initialize the SQL database connection."""
    # allow minimal schema sampling (fixes sql_db_schema tool failures)
    return SQLDatabase.from_uri(
        db_uri,
        sample_rows_in_table_info=2
    )


def init_toolkit(db: SQLDatabase, llm):
    """Initialize SQL toolkit with LLM and DB."""
    return SQLDatabaseToolkit(db=db, llm=llm)


# ==========================================================
# 🧠 3️⃣ Memory Saver
# ==========================================================
GLOBAL_MEMORY = MemorySaver()


# ==========================================================
# 🧠 4️⃣ System Prompt
# ==========================================================
SYSTEM_PROMPT = """You are **DataBuddy 🧠**, an intelligent assistant that can chat naturally and perform SQL queries.
You are connected to a SQL database.

Guidelines:
- Always call tools using proper JSON (e.g. {"table_names": ["students"]})
- Never guess table names — first call sql_db_list_tables to check.
- Write and execute SQL using available tools.

- Format results as Markdown tables.
- If a tool fails, say “That table might not exist or may be inaccessible.”
- Be concise and conversational.
"""


# ==========================================================
# 🪶 5️⃣ Summarization Middleware
# ==========================================================
# async def summarize_if_needed(messages, llm, max_messages=4, summarize_every=4):
#     """
#     Summarize chat every N messages to prevent context overflow.
#     Keeps conversation memory compact for long sessions.
#     """
#     if len(messages) <= max_messages or len(messages) % summarize_every != 0:
#         return messages

#     text = get_buffer_string(messages[:-3])
#     summary_prompt = f"Summarize this past chat briefly for context:\n{text}"
#     summary_response = await llm.ainvoke(summary_prompt)
#     summary = summary_response.content
#     return [SystemMessage(content=f"Previous conversation summary:\n{summary}")] + messages[-3:]


# def make_summarize_middleware(llm, max_messages=4, summarize_every=4):
#     """Return @before_model middleware bound to this LLM."""
#     @before_model
#     async def summarize_context(state, runtime):
#         new_messages = await summarize_if_needed(
#             state["messages"],
#             llm=llm,
#             max_messages=max_messages,
#             summarize_every=summarize_every
#         )
#         state["messages"] = new_messages
#         return state
#     return summarize_context


# ==========================================================
# ⚙️ 6️⃣ Agent Creation
# ==========================================================
def create_data_agent(llm, toolkit, checkpointer):
    """Create DataBuddy Agent with memory + summarization."""
    # summarize_context = make_summarize_middleware(llm)
    return create_agent(
        llm,
        tools=toolkit.get_tools(),
        system_prompt=SYSTEM_PROMPT,
         checkpointer=checkpointer,
        middleware=[ SummarizationMiddleware(
            model=llm,
            max_tokens_before_summary=1000,  # Trigger summarization at 4000 tokens
            messages_to_keep=3,  # Keep last 20 messages after summary
            summary_prompt="Custom prompt for summarization...",  # Optional
        ),]
       
    )


# ==========================================================
# 🚀 7️⃣ Async Run Logic
# ==========================================================
async def run_chat(
    model_name: str,
    provider: str,
    api_key: str,
    db_uri: str,
    user_query: str,
    thread_id: Optional[str] = "demo_thread_1",
):
    """Async entrypoint for running DataBuddy."""
    llm = init_llm(model_name, provider, api_key)
    db = init_database(db_uri)
    toolkit = init_toolkit(db, llm)
    checkpointer = GLOBAL_MEMORY
    agent = create_data_agent(llm, toolkit, checkpointer)

    # Run query with memory persistence per thread_id
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": user_query}]},
        config={"configurable": {"thread_id": thread_id}}
    )

    result = response["messages"][-1].content
    print("\n🤖 DataBuddy:")
    print(result)
    return result
