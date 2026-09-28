# Knowledge Library: capturing the unwritten playbook

Today the know-how for writing strong records lives in PDFs passed around by email and in the heads of experienced supervisors. Examples: "how to show growth year over year," "lead with selection over peers," "quantify impact within the first 30 days in a new role." The library turns that knowledge into something the AI uses every time someone writes or reviews.

## What gets uploaded
| Type | Examples | Typical scope |
|---|---|---|
| Writing guides | "Building a promotable record," narrative statement guides, abbreviation lists | Wing / group |
| Award SOPs | Quarterly award memo, format and category rules | Squadron / group |
| Example packages | Past winners, **sanitized** | Squadron and up |
| Unit context | Commander's priorities, mission brief | Squadron / flight |
| Personal | The member's own prior evaluations and awards | Personal only |

## How it's used
- **Coach:** "Your entry says you took over a new role. Guides in your library recommend showing selection over peers and early impact. How many people were considered? What changed in the first 30 days?"
- **Scorer:** rubric criteria can be tied to library guidance, and every score cites where the standard came from.
- **Editor:** suggests rewrites in the patterns the unit's guides teach, citing the guide.
- **Setup guide:** reads an uploaded award SOP to pre-fill format rules.
- **Growth view:** compares a member's records across years (their personal scope only) to surface growth.

## Governance
- Every document has a **scope** (who can retrieve it), an **owner**, a **version**, and a **status** (draft → approved → retired). Only approved documents feed the AI.
- The SEL (or the wing/group admin at their level) approves unit-wide documents. Personal uploads are visible only to their owner.
- **Example packages must be sanitized** (`ai/assist/sanitizer`) and human-approved before sharing. Names, EDIPIs and other PII are removed.
- Uploads are malware-scanned and stored through the storage adapter (S3 / Blob) with customer-managed keys.
- Supersession: uploading a new version of a guide retires the old one from retrieval.
