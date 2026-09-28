# Domain Model

```
OrgUnit (Wing > Group > Squadron > Flight > Section)   self-referencing tree
  ├──< UnitContext (mission, priorities, focus areas; feeds the AI)
  ├──< UnitRoleAssignment (member, role: CC | SEL | FLIGHT_CC | FLIGHT_CHIEF | SUPERVISOR | BOARD, dates)
  ├──< AwardProgram ──< AwardRuleVersion (format, sections, rubric, advances_to)
  │        ├──< AwardEligibility (which OrgUnits can apply, + optional criteria)
  │        └──< AwardCycle (e.g. FY27 Q1) ──< CycleMilestone (step, due date)
  └──< RoutingTemplate ──< RoutingStep

Member ──< Assignment (duty title, OrgUnit, supervisor, dates)
   ├──< Entry (journal) ──< Attachment
   ├──< Bullet ──< BulletVersion   (author: MEMBER | AI | REVIEWER)
   │      └──>< Entry              (traceability)
   └──< Package (kind: NOMINATION | EVALUATION, cycle or rating period, optional category)
          ├──< PackageItem ──> Bullet   (section, position)
          ├──< RoutingEvent (submit, return, forward, approve; who, when, note)
          ├──< Comment (anchored to text span, threaded, resolved?)
          └──< AiAssessment (rubric scores + reasons, model/prompt version)
```

## Key rules
- A member sees an award if their unit (or a parent unit with `includes_subunits`) is on its eligibility list and they meet any optional criteria.
- Awards chain by `advances_to` (flight > squadron > group > wing), which forms the nomination ladder.
- Rules are inherited down the org tree (wing > group > squadron), and the lowest override wins.
- An award cycle pins a rule version, so later edits don't change packages already in flight.
- Entries can support many packages across overlapping periods.
- Supervisors only see packages, never the private journal behind them.
