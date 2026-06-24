from .debate.against_opening import against_opening_agent
from .debate.against_rebuttal_agent import against_rebuttal_agent
from .debate.pro_opening import pro_opening_agent
from .debate.pro_rebuttal_agent import pro_rebuttal_agent
from .judge import judge_agent
from .research import research_agent
from .moderator import moderator_agent


__all__= [
    "against_rebuttal_agent",
    "against_opening_agent",
    "pro_opening_agent",
    "pro_rebuttal_agent",
    "judge_agent",
    "research_agent",
    "moderator_agent"
]