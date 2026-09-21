# Final Project WBS and Progress

Progress snapshot: September 20, 2026. Current repository work is implemented and locally verified; the recording, group review, and final submission remain.

## Status and Evidence

- `[x]`: present in the saved project and checked locally.
- `[ ]`: still requires group action or submission evidence.

The saved notebook contains 19 code cells. An isolated top-to-bottom execution completed with execution counts 1–19 and no error outputs. A separate booking check reduced PA1002 from 80 to 79 seats in a test database, and the manual reset restored it to the CSV value of 90. The tracked database remains valid with 20 flight records.

## Scope Sources

- **S1**: Project Specification — required components and minimum functional workflow.
- **S2**: Project Specification — deliverables and submission instructions.
- **R1–R8**: Student Rubric — core functionality, pricing logic, course concepts, persistence/data, robustness, code quality, README, and recorded demo.

## 1 Potter Airlines Dynamic Pricing Submission

### 1.1 Flight Data and Inputs

- [x] **1.1.1 Reusable fictional dataset** — `flights.csv` contains 20 flights with identifiers, routes, departure dates, fare inputs, capacities, remaining seats, demand factors, and seasonal factors. Sources: S1, R4.
- [x] **1.1.2 Loaded and date-prepared flight table** — the notebook loads the CSV, converts `departure_date`, calculates `days_until_departure`, and excludes already-departed flights from pricing. Sources: S1, R1.

### 1.2 Explainable Pricing Capabilities

- [x] **1.2.1 Bounded five-factor pricing** — the `Flight` method combines base fare, time, capacity, demand, and seasonality, then applies the CAD 45–1,500 limits and two-decimal rounding. Sources: S1, R2, R3.
- [x] **1.2.2 Meaningful vectorized calculation** — Pandas/NumPy calculates time, load, capacity, raw-price, and final-price columns without looping through flights. Sources: S1, R3.
- [x] **1.2.3 Batch fare results and consistency check** — every eligible flight receives a fare, and PA1002's vectorized result is checked against `Flight.calculate_price`. Sources: S1, R1, R2.

### 1.3 Flight Objects and Operational Behavior

- [x] **1.3.1 Meaningful `Flight` class and reusable functions** — the class holds flight state and provides load-factor, seat-update, pricing, and dictionary-conversion methods. Sources: S1, R3.
- [x] **1.3.2 Explainable operational change** — the notebook demonstrates that selling seats increases occupancy and changes the calculated fare. Sources: S1, R1, R2.

### 1.4 SQLite Persistence

- [x] **1.4.1 Flight database schema** — an explicit `CREATE TABLE` schema stores the required flight fields and can be rebuilt from the CSV. Sources: S1, R4.
- [x] **1.4.2 Parameterized CRUD operations** — the notebook demonstrates parameterized INSERT, SELECT, UPDATE, and DELETE with read-back assertions. Sources: S1, R1, R4.
- [x] **1.4.3 Safe seat persistence** — database updates reject unknown flight IDs and remaining-seat values outside `0..capacity`. Sources: S1, R5.

### 1.5 Flight Search and User Workflow

- [x] **1.5.1 Filtered and ranked results** — sold-out flights are removed and available flights are ranked by final price. Sources: S1, R1.
- [x] **1.5.2 Interactive booking workflow** — the user can choose a destination and flight, view current prices, book one seat, and persist the new seat count to SQLite. Sources: S1, R1.
- [x] **1.5.3 Reproducible manual reset** — the reset function restores the database from `flights.csv` only when deliberately called. Sources: S1, R6.

### 1.6 Validation and Reproducibility

- [x] **1.6.1 Input and edge-case checks** — the notebook checks capacity, seat range, base fare, positive factors, negative departure intervals, missing data, duplicate flight IDs, invalid database updates, and sold-out booking attempts. Sources: S1, R5.
- [x] **1.6.2 Fare assertions and checked evidence** — fare bounds are asserted, object and vectorized prices are reconciled, and database updates are read back and verified. Sources: S1, R5.
- [x] **1.6.3 Runnable and readable notebook** — the notebook is organized into six numbered sections and completed an isolated top-to-bottom execution with no error outputs. Interactive booking and reset are manual so `Run All` does not wait for input or erase booking changes. Sources: S1, S2, R1, R6.

### 1.7 Submission Documentation and Demonstration

- [x] **1.7.1 Final README** — setup, data flow, pricing rules, SQLite behavior, manual booking/reset instructions, validation, and limitations reflect the current notebook. Sources: S2, R7.
- [ ] **1.7.2 Recorded demonstration** — record 4–5 minutes showing system execution, a pricing decision, meaningful code, and one checked edge case or bug. Sources: S2, R8.
- [ ] **1.7.3 Final group review** — confirm team members understand their demonstration sections and approve the saved submission files. Sources: S2.
- [ ] **1.7.4 Group submission package** — submit the runnable notebook, required data/database files, README, and recording through the course channel by October 2, 2026. Sources: S2.

## Boundaries and Decisions

- Website, GUI, authentication, deployment, advanced ML/optimization, dashboards, and LLM/API features remain outside the required scope.
- `flights.csv` is the reproducible initial data source; `potter_airlines.db` is the persistent store; `potter_airlines.ipynb` contains the processing and user workflow.
- The fixed quote date (`2026-09-19`) and CAD 45–1,500 bounds are documented project choices used consistently.
- The booking and reset calls remain commented by default. They are run manually because one waits for user input and the other intentionally discards saved booking changes.

## Requirement Coverage Review

| Requirement | Packages |
| --- | --- |
| Flight inputs, CSV loading, and date preparation | 1.1.1–1.1.2 |
| Explainable bounded prices and multiple-flight fares | 1.2.1–1.2.3 |
| Meaningful functions and class | 1.2.1, 1.3.1 |
| Meaningful Pandas/NumPy vectorization | 1.2.2 |
| SQLite schema and parameterized CRUD | 1.4.1–1.4.3 |
| Filter, ranking, and interactive workflow | 1.5.1–1.5.3 |
| Validation, assertions, and edge cases | 1.6.1–1.6.3 |
| README, recording, review, and submission | 1.7.1–1.7.4 |

All required implementation components in the supplied specification and rubric are mapped above. Remaining unchecked work requires the group recording, review, and submission rather than additional core implementation.
