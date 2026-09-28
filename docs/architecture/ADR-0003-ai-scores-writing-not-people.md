# ADR-0003: AI scores the writing, not the person

**Status:** Proposed

**Context:** AI-assisted rating of award packages is valuable but has fairness and Responsible AI implications.

**Decision:**
- The AI scorer evaluates package quality against the award's published rubric (action, impact, metrics, clarity, compliance) and explains each score.
- AI scores are coaching tools for members and supervisors. They are **never** shown to boards, never rank nominees, and never auto-select winners.
- All AI outputs are logged with model version and prompt version, and bias is evaluated in `ai/evaluation/`.

**Consequences:** This makes the Responsible AI story stronger for the AI Factory pitch. Board scoring stays fully human.
