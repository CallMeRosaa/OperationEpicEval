# Coordination Workflow

A **Nomination** (award) or **Evaluation Draft** is a package that moves through a **routing chain**. The routing chain comes from the unit's routing template. People are resolved from the org structure at routing time, e.g., "FIRST_SUPERVISOR of this member".

```
         ┌──────────── return with edits ◀───────────┐
         ▼                                           │
 DRAFT ─▶ SUBMITTED ─▶ SUPERVISOR_REVIEW ─▶ FLIGHT_COORD ─▶ SEL_APPROVAL ─▶ NOMINATED ─▶ BOARD ─▶ RESULT
 member   (notifies)   1st supervisor        flight lead.     SEL            (advances_to next level?)
```

## At every review step the reviewer can
- See **who submitted it, when, and what changed** since the last round (diff).
- Leave **inline comments** anchored to specific text.
- Make **suggested edits** (tracked changes) or ask the AI editor for them.
- Run the **AI scorer** against the award rubric and see the per-criterion reasons.
- **Return** it to the previous step or to the member, **or forward** it with a note.

## Rules
- The rules engine blocks submission when the format is violated (e.g., 6 statements instead of 5, or a statement over 6 lines).
- Suspense dates come from the cycle's milestones. Overdue items escalate to the next role.
- Every action is an immutable `routing_event` for audit and history.
- Members can see the status of their own package. Board scores and competitor packages are not visible to nominees.
