# Vague Response Escalation Table

Shared knowledge file for handling vague or abstract answers during interviews. Referenced by ideate, jtbd-extractor, feature-brief, and assumption-audit.

## Escalation Patterns

| Vague pattern | Reaction |
|---|---|
| "it should be fast" | "In the story you told me, how long did it take? How long should it take for the user not to complain?" |
| "needs to be secure" | "Secure against what? Last time something went wrong, what happened?" |
| "easy to use" | "Describe someone who would struggle. What would they try and where would they get stuck?" |
| "needs to scale" | "How many simultaneous users today? In 12 months? In 3 years?" |
| "many/few/several" | "Give me a number. Order of magnitude: tens, hundreds, thousands?" |
| "we'll figure that out later" | "Does this block implementation? If yes, I need a decision. If no, I'll register as ASM-# deferred with deadline." |
| "like [competitor]" | "What exactly from [competitor]? What do you NOT want from it?" |
| "obvious/standard" | "Explain the 'obvious' as if I've never seen the system." |
| "real-time" | "Real-time means what latency? < 100ms? < 1s? < 5s?" |
| "robust" | "Handles which specific failures with which specific behavior?" |

## Usage Rule

When an answer matches any pattern above:
1. Fire the corresponding escalation question
2. Increment `vague_count` in `elicitation-state.yaml`
3. If 3+ consecutive vague answers: trigger reflection checkpoint
