from graph import graph
from models import DebateMessage
from textwrap import wrap

result = graph.invoke(
    {
        "topic": "Should AI replace software engineers?",
        "research": "",
        "conversation_history": [
            DebateMessage(agent="system", message="debate started")
        ],
        "verdict": ""
    }
)

print("\n" + "=" * 100)
print(f"TOPIC: {result['topic']}")
print("=" * 100)

print("\n📚 RESEARCH\n")
print(result["research"])

print("\n" + "=" * 100)
print("DEBATE TRANSCRIPT")
print("=" * 100)

for msg in result["conversation_history"]:

    title = f" {msg.agent.upper()} "

    print("\n" + "╔" + "═" * 98 + "╗")
    print("║" + title.center(98) + "║")
    print("╠" + "═" * 98 + "╣")

    for line in msg.message.split("\n"):
        wrapped = wrap(line, width=94) or [""]
        for w in wrapped:
            print(f"║ {w:<94} ║")

    print("╚" + "═" * 98 + "╝")

print("\n" + "=" * 100)
print("🏆 VERDICT")
print("=" * 100)

print(result["verdict"])