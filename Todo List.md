# Final Project WBS and Progress

Progress snapshot: September 16, 2026. Draft for group review; no owners or schedule assigned.

## Status and Evidence

- `[x]`: present in the saved files and checked locally.
- `[ ]` with **In progress**: partially present or still needing final evidence.
- Other unchecked items: not present in the current saved notebook.

VS Code Save All was performed. The latest notebook contains five code cells: a time-factor function, Flight class, rejected seat-update example, before/after pricing example, and an invalid-constructor test. Targeted checks verified five-factor pricing, fare bounds, day thresholds, constructor guards and seat-change behavior. All five saved code cells now pass a clean sequential execution. The corrected invalid-constructor test supplies route arguments and catches ValueError for an out-of-range seat count.

Earlier CSV-loading, vectorized-factor and date-preparation cells are absent from this saved version. They were completed earlier but must be restored or rewritten before those deliverables can be checked again. Student code was not rewritten during this review.

## Scope Sources

- **S1**: Project Specification — required components and minimum functional workflow.
- **S2**: Project Specification — deliverables and submission instructions.
- **R1–R8**: Student Rubric — core functionality, pricing logic, course concepts, persistence/data, robustness, code quality, README, recorded demo, respectively.

## 1 Potter Airlines Dynamic Pricing Submission

### 1.1 Flight Data and Inputs

- [x] **1.1.1 Reusable fictional dataset** — 20 flights in `flights.csv`, with identifiers, routes, dates, fare inputs, seats, capacity, demand and seasonal factors. Basic CSV validity checked. Sources: S1, R4.
- [ ] **1.1.2 Loaded and date-prepared flight table** — **Previously completed; absent from current notebook.** Restore CSV loading, datetime conversion and departure intervals before checking complete. Sources: S1, R1.

### 1.2 Explainable Pricing Capabilities

- [x] **1.2.1 Bounded five-factor pricing function/method** — Saved method uses base fare, time, capacity, demand and seasonality; local checks verified two-decimal results and CAD 45–1,500 bounds. Sources: S1, R2, R3.
- [ ] **1.2.2 Meaningful vectorized multi-flight calculation** — **Previously completed; absent from current notebook.** Restore whole-column load/capacity calculations and verify them across the CSV. Sources: S1, R3.
- [ ] **1.2.3 Complete batch fare results** — every flight receives a calculated fare using its own inputs and departure interval. Sources: S1, R1, R2.

### 1.3 Flight Objects and Operational Behavior

- [x] **1.3.1 Meaningful Flight class and reusable functions** — saved class holds state and provides load factor, seat update and pricing methods; separate time-factor function exists. Sources: S1, R3.
- [x] **1.3.2 Explainable operational change demonstration** — Saved example verifies 18 to 13 seats and fares 556.38 to 561.33 at a constant 12-day interval. Sources: S1, R1, R2.

### 1.4 SQLite Persistence

- [ ] **1.4.1 Flight database schema** — explicit CREATE TABLE covering the relevant project data, with reproducible setup. Sources: S1, R4.
- [ ] **1.4.2 Parameterized data operations** — demonstrated INSERT, SELECT, UPDATE and DELETE with separately supplied values, plus read-back evidence. Sources: S1, R1, R4.

### 1.5 Flight Search and Presentation

- [ ] **1.5.1 Useful filtered or ranked results** — understandable output for a destination/budget/availability query or a ranking. Exclude sold-out flights from bookable results. Sources: S1, R1.

### 1.6 Validation and Reproducibility

- [ ] **1.6.1 Input and edge-case checks** — **In progress.** Capacity, seat range, base fare, positive factors, negative days and seat-update guards verified locally. The invalid-constructor demonstration now passes; integer seat counts and missing/non-finite data still need consideration for complete input validation. Sources: S1, R5.
- [ ] **1.6.2 Fare assertions and checked edge-case evidence** — **In progress.** Saved negative-day and illegal-seat-update examples work; local review verified fare limits and threshold days. The final constructor demonstration now works; explicit fare assertions are not yet in the notebook. Sources: S1, R5.
- [ ] **1.6.3 Final runnable and readable submission** — **In progress.** The current five-cell example passes sequential execution; input loading is absent and the full workflow is incomplete. Final acceptance requires a successful fresh-kernel run of the complete system. Sources: S1, S2, R1, R6.

### 1.7 Submission Documentation and Demonstration

- [ ] **1.7.1 Final README** — **In progress.** English draft exists; update it to match completed behavior, dependencies, setup, pricing choices and limitations. Sources: S2, R7.
- [ ] **1.7.2 Recorded demonstration** — 4–5 minutes showing system execution, pricing decisions, meaningful code, and one checked edge case/bug. Sources: S2, R8.
- [ ] **1.7.3 Group submission package** — runnable code, necessary data/schema, final README and one recording submitted through the course channel by October 2, 2026. Sources: S2.

## Boundaries and Open Decisions

- Website, GUI, authentication, deployment, advanced ML/optimization, dashboards and LLM/API features are optional and outside this current draft scope.
- JSON and `to_dict()` are useful intermediate techniques, but JSON is not a required final deliverable. Their absence alone does not make the project incomplete.
- The fixed quote date and CAD 45–1,500 bounds are project choices. They should be documented and used consistently.
- Owner for all unchecked packages: unassigned; the group can divide responsibilities later.
- SQLite update demonstrations and class update demonstrations share business rules but have distinct acceptance evidence: database persistence versus in-memory state.
- Save reconciliation is complete. Current checklist reflects the latest saved notebook; missing earlier data-preparation cells remain visible.

## Requirement Coverage Review

| Requirement | Packages |
| --- | --- |
| Flight inputs and CSV loading | 1.1.1–1.1.2 |
| Explainable bounded prices and multiple-flight fares | 1.2.1, 1.2.3 |
| Meaningful functions and class | 1.2.1, 1.3.1 |
| Meaningful Pandas/NumPy vectorization | 1.2.2 |
| SQLite schema and parameterized CRUD | 1.4.1–1.4.2 |
| Filter/rank and display results | 1.5.1 |
| Operational update and effect | 1.3.2, 1.4.2 |
| Validation/assertions and edge case | 1.6.1–1.6.2 |
| Runnable source and readable code | 1.6.3 |
| README, recording and group submission | 1.7.1–1.7.3 |

All required components in the supplied specification and rubric are mapped above. This is a scope coverage review, not a claim that they are implemented. No estimated completion percentage, duration or grade is assigned.
