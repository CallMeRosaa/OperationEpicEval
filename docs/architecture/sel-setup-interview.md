# SEL Setup Interview (5–10 minutes)

A guided conversation, run by the AI setup guide or a plain step-by-step form, that turns what the SEL already knows into the unit's rulebook. The output looks like `config/award-rules/96mxs.example.yaml`. The SEL reviews a summary and publishes it.

## Flow
1. **Confirm the unit.** "You're the SEL for 96 MXS under 96 MXG. Is that right?" This is pre-filled from the org tree.
2. **Map the sub-units.** "What flights or sections make up your squadron?" For example: Munitions Flight, PMEL Flight. Any new sub-units get added to the org tree.
3. **List the awards.** "Which awards does your squadron run or nominate for?" The SEL picks from awards the group or wing already publishes, or adds new ones.
4. **Set eligibility for each award.** "Who can apply for this one?" The SEL ticks flights and sections on the org tree. An optional narrower rule can be added, like "Inspectors only."
5. **Set the format for each award.** "How many statements? Max lines each? Bullet or narrative? Any required sections?" The group or wing format is pre-filled when it exists. The SEL can upload the award SOP or memo, and the AI pulls the rules out for the SEL to confirm.
6. **Set the routing.** "Who sees a draft after the member?" Default: first supervisor > flight leadership > SEL > board.
7. **Set the suspense dates.** "When are drafts due to flight leadership?" The SEL can give fixed dates or offsets from the end of the period.
8. **Add unit context (optional).** Mission and the commander's current priorities. The AI uses these when coaching and scoring.
9. **Review and publish.** The SEL sees a one-page summary, edits it, and publishes. Publishing creates rule version 1. Cycles open on schedule.

## Principles
- **Inherit first.** Anything the group or wing already defined is pre-filled, and the SEL only overrides what differs.
- **Eligibility is org-scoped.** "These flights can apply for this award" covers most cases. Narrower criteria are optional.
- **Layered awards.** Every award can say where its winner goes next (flight > squadron > group > wing). That builds the nomination ladder automatically.
- **Re-runnable.** The SEL can rerun any step later. Changes create a new rule version, and cycles already in progress keep the version they started with.
