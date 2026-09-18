# Final Project WBS and Progress

Progress snapshot: September 18, 2026. Draft for group review; no owners or schedule assigned.

## Status and Evidence

- `[x]`: present in the saved files and checked locally.
- `[ ]` with **In progress**: partially present or still needing final evidence.
- Other unchecked items: not present in the current saved notebook.

The saved notebook contains ten code cells and passes sequential execution. SQLite setup imports 20 CSV flights and demonstrates parameterized INSERT, SELECT, UPDATE and DELETE, with read-back assertions. The demo setup rebuilds the table on each run. CSV loading is present; date preparation, vectorized calculations and batch pricing remain pending.

## Scope Sources

- **S1**: Project Specification — required components and minimum functional workflow.
- **S2**: Project Specification — deliverables and submission instructions.
- **R1–R8**: Student Rubric — core functionality, pricing logic, course concepts, persistence/data, robustness, code quality, README, recorded demo, respectively.

## 1 Potter Airlines Dynamic Pricing Submission

### 1.1 Flight Data and Inputs

- [x] **1.1.1 Reusable fictional dataset** — 20 flights in `flights.csv`, with identifiers, routes, dates, fare inputs, seats, capacity, demand and seasonal factors. Basic CSV validity checked. Sources: S1, R4.
- [ ] **1.1.2 Loaded and date-prepared flight table** — **Previously completed; absent from current notebook.** CSV loading is restored; datetime conversion and departure intervals remain pending. Sources: S1, R1.

### 1.2 Explainable Pricing Capabilities

- [x] **1.2.1 Bounded five-factor pricing function/method** — Saved method uses base fare, time, capacity, demand and seasonality; local checks verified two-decimal results and CAD 45–1,500 bounds. Sources: S1, R2, R3.
- [ ] **1.2.2 Meaningful vectorized multi-flight calculation** — **Previously completed; absent from current notebook.** Restore whole-column load/capacity calculations and verify them across the CSV. Sources: S1, R3.
- [ ] **1.2.3 Complete batch fare results** — every flight receives a calculated fare using its own inputs and departure interval. Sources: S1, R1, R2.

### 1.3 Flight Objects and Operational Behavior

- [x] **1.3.1 Meaningful Flight class and reusable functions** — saved class holds state and provides load factor, seat update and pricing methods; separate time-factor function exists. Sources: S1, R3.
- [x] **1.3.2 Explainable operational change demonstration** — Saved example verifies 18 to 13 seats and fares 556.38 to 561.33 at a constant 12-day interval. Sources: S1, R1, R2.

### 1.4 SQLite Persistence

- [x] **1.4.1 Flight database schema** — explicit CREATE TABLE covering the relevant project data, with reproducible setup. Sources: S1, R4.
- [x] **1.4.2 Parameterized data operations** — demonstrated INSERT, SELECT, UPDATE and DELETE with separately supplied values, plus read-back evidence. Sources: S1, R1, R4.

### 1.5 Flight Search and Presentation

- [ ] **1.5.1 Useful filtered or ranked results** — understandable output for a destination/budget/availability query or a ranking. Exclude sold-out flights from bookable results. Sources: S1, R1.

### 1.6 Validation and Reproducibility

- [ ] **1.6.1 Input and edge-case checks** — **In progress.** Capacity, seat range, base fare, positive factors, negative days and seat-update guards verified locally. The invalid-constructor demonstration now passes; integer seat counts and missing/non-finite data still need consideration for complete input validation. Sources: S1, R5.
- [ ] **1.6.2 Fare assertions and checked edge-case evidence** — **In progress.** Saved negative-day and illegal-seat-update examples work; local review verified fare limits and threshold days. The final constructor demonstration now works; explicit fare assertions are not yet in the notebook. Sources: S1, R5.
- [ ] **1.6.3 Final runnable and readable submission** — **In progress.** The current ten-cell notebook passes sequential execution; CSV loading and standalone SQLite operations work, but the complete pricing workflow remains incomplete. Final acceptance requires a successful fresh-kernel run of the complete system. Sources: S1, S2, R1, R6.

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
- Save reconciliation is complete. Current checklist reflects the latest saved notebook; pending date preparation and vectorized calculations remain visible.

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
