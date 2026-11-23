"""One LangGraph agent + one tool node + chat memory."""
import os
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from .tools import get_policy, create_ticket

TOOLS = [get_policy, create_ticket]
llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
    temperature=0,
)
llm_with_tools = llm.bind_tools(TOOLS)


def agent_node(state: MessagesState):
    """Ask Groq for the next response or a tool call."""
    instructions = SystemMessage(content=(
        "You are a friendly university helpdesk assistant. "
        "Use get_policy for attendance, library, and fee rules. "
        "Use create_ticket only when the user clearly requests a complaint. "
        "This is a fictional university demo. Be brief and clear."
    ))
    answer = llm_with_tools.invoke([instructions, *state["messages"]])
    return {"messages": [answer]}


builder = StateGraph(MessagesState)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(TOOLS))
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile(checkpointer=InMemorySaver())
