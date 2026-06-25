from graph import graph
from models import DebateMessage, DebateState
from textwrap import wrap

init_stage: DebateState = {
        "topic": "Should AI replace software engineers?",
        "research": "",
        "conversation_history": [
            DebateMessage(agent="system", message="debate started")
        ],
        "verdict": {},
        "supporting_evidence": {}
    }

result = graph.invoke(init_stage)

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

verdict = result["verdict"]

print("Winner:", verdict["winner"])
print("Reasoning:", verdict["reasoning"])
print("Pro Score:", verdict["pro_score"])
print("Against Score:", verdict["against_score"])

print("\n" + "=" * 100)
print("🏆 Supporting_evidence")
print("=" * 100)
evidence = result["supporting_evidence"]

print("Argument:")
print(evidence["argument"])

print("\nEvidence:")
for item in evidence["evidence"]:
    print("-", item)

print("\nConfidence:")
print(evidence["confidence"])