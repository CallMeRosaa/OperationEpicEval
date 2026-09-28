# Domain Model

```
Member ──< Assignment (job/duty title, unit, dates)
   │
   ├──< Entry (the journal) ──< Attachment
   │      date, title, what I did, impact, metrics, tags, assignment
   │
   ├──< RatingPeriod (type: QUARTERLY_AWARD | SEMIANNUAL | ANNUAL_EVAL, start, end)
   │      └──< Package (award package or evaluation draft)
   │             └──< PackageItem ──> Bullet
   │
   ├──< Bullet ──< BulletVersion (text, author: member|ai|rater, accepted?)
   │      └──>< Entry   (every bullet traces back to its source entries)
   │
   └──< RatingChainLink (supervisor / rater / additional rater, effective dates)
            └── Review (comments, status, sign-off on a Package)
```

## Key rules
- An entry can support many bullets, and a bullet can come from many entries.
- Rating periods can overlap. One entry can count toward a quarterly award AND the annual evaluation.
- Rating-chain access is time-bound. A former supervisor loses access when the link ends.
- AI-generated text is always stored as a `BulletVersion` with `author = 'ai'` until a human accepts it.
