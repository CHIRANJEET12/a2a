from langgraph.graph import StateGraph, END
from models import DebateState
from agents import moderator_agent, research_agent, pro_opening_agent, pro_rebuttal_agent, against_opening_agent, against_rebuttal_agent, judge_agent


# CREATION OF STATEGRAPH
builder = StateGraph(DebateState)


# ADDING OF NODES
builder.add_node(
    "moderator",
    moderator_agent
)
builder.add_node(
    "research", 
    research_agent
)

builder.add_node(
    "pro_opening",
    pro_opening_agent
)

builder.add_node(
    "against_opening",
    against_opening_agent
)

builder.add_node(
    "pro_rebuttal",
    pro_rebuttal_agent
)

builder.add_node(
    "against_rebuttal",
    against_rebuttal_agent
)

builder.add_node(
    "judge", 
    judge_agent
)


# ENTRY POINT
builder.set_entry_point("moderator")

builder.add_edge(
    "moderator",
    "research"
)

# EDGES FROM NODE TO NODE
builder.add_edge(
    "research",
    "pro_opening"
)

builder.add_edge(
    "pro_opening",
    "against_opening"
)

builder.add_edge(
    "against_opening",
    "pro_rebuttal"
)

builder.add_edge(
    "pro_rebuttal",
    "against_rebuttal"
)

builder.add_edge(
    "against_rebuttal",
    "judge"
)

builder.add_edge(
    "judge",
    END
)

graph = builder.compile()
