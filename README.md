# Potter Airlines Dynamic Pricing Project

RSM8431 — Team 15

This Python project prices Potter Airlines flights dynamically based on explainable business signals: time to departure, remaining capacity, route demand, and seasonality. It is a coursework project using fictional flight data and explainable pricing rules.

## Purpose

Two passengers booking the same flight can see different fares because they book at different times, remaining capacity has changed, or demand for the route differs. This project shows how a small set of transparent factors produces that behaviour, using a `Flight` class, SQLite persistence, and vectorized Pandas/NumPy calculations across the whole flight table.

## Files

| File | Purpose |
| --- | --- |
| `potter_airlines.ipynb` | Main runnable notebook: pricing helpers, `Flight` class, SQLite persistence, vectorized pricing, validation, and an interactive booking workflow. |
| `potter_airlines.db` | SQLite database initialized on first use; saved bookings survive Run All. |
| `flights.csv` | Twenty fictional flights used as the input dataset. Fares are in Canadian dollars (CAD). |
| `Potter_Airlines_Project_Specification.docx` | Assignment requirements. |
| `Potter_Airlines_Student_Rubric.docx` | Grading criteria. |

The CSV includes flight identifiers, origins, destinations, departure dates, base fares, total capacity, remaining seats, demand factors, and seasonal factors. It includes a sold-out flight (PA1007), flights with very few seats remaining, and flights that have already departed relative to the notebook's fixed quote date.

## Setup and Run

1. Clone or download this repository.
2. Use a Python environment with Pandas, NumPy, and a Jupyter-compatible notebook runner. In VS Code, install the Python and Jupyter extensions and select your Python environment as the notebook kernel.
3. Install the packages in that environment if needed:

   ```bash
   python -m pip install pandas numpy ipykernel
   ```

4. Keep `flights.csv` in the same folder as `potter_airlines.ipynb`, and run the notebook with that folder as the working directory.
5. Restart the kernel and run all cells from top to bottom. The non-interactive workflow runs cleanly in sequence; the SQLite setup creates the flights table from CSV only if it does not exist. Existing bookings are preserved, and the seat-sale demonstration is manual.
6. To use the command-line booking demo, remove the `#` from `# run_interactive_booking()` and run that cell manually.
7. To demonstrate a 10-seat sale, uncomment the `simulate_seat_sale(...)` call in section 5.5 and run that cell manually. Each execution sells another 10 seats from current inventory.
8. To discard booking changes and restore the original CSV data, remove the `#` from `# reset_database_to_initial_state()` and run the reset cell manually.

No external API, LLM service, or API key is needed to run this notebook.

## Workflow

1. **Single-flight pricing (`Flight` class).** Demonstrates the pricing formula, a seat update, and input validation on one hand-built flight.
2. **SQLite persistence.** On first use, loads `flights.csv`, validates each row through the `Flight` class, and inserts it (`Flight` → `to_dict()` → parameterized `INSERT`) into a `flights` table created with an explicit schema, using a `cursor` object and explicit `commit()`/`close()` calls. Demonstrates parameterized `SELECT`, `UPDATE`, and `DELETE` on a temporary test row, then reads the table back into a DataFrame.
3. **Batch pricing (vectorized).** Converts `departure_date` to real dates, computes `days_until_departure`, checks the whole table's assumptions with `assert`, excludes already-departed flights, and prices every remaining flight at once using `np.select`, whole-column arithmetic, and `np.clip` — no `for` loop over flights. A cross-check confirms the vectorized price agrees with `Flight.calculate_price` for the same flight.
4. **Filter and rank.** Excludes sold-out flights and ranks the rest by price.
5. **Operational update (manual).** Sells 10 seats on PA1002 using its current database inventory. A transaction reads the current row, deducts seats with a conditional parameterized `UPDATE`, and verifies the result. Insufficient inventory rolls back the sale. The displayed fares use the current before/after seat counts.
6. **Edge case.** Attempts to sell a seat on the already sold-out PA1007 and shows it is rejected.
7. **Interactive booking system.** A command-line `while` loop fetches current data from SQLite, prompts for a destination and flight, asks how many tickets to purchase, and reduces `seats_remaining` by the validated quantity.
8. **Manual reset.** A separate reset function rebuilds the database from `flights.csv` when the group wants to start a fresh demonstration. All input rows are validated before rebuilding; an explicit transaction rolls back the rebuild if insertion fails. It is not called automatically, so a completed booking remains saved until the reset is run deliberately.

## Pricing logic

```text
load_factor = 1 - seats_remaining / capacity
capacity_factor = 1 + 0.45 * load_factor
price = base_fare * time_factor * capacity_factor * demand_factor * seasonal_factor
```

| Days until departure | Time factor |
| --- | --- |
| 0–7 | 1.35 |
| 8–21 | 1.10 |
| More than 21 | 1.00 |

Higher occupancy raises the capacity factor; a shorter booking window raises the time factor. Demand and seasonal factors are positive multipliers supplied in the CSV. Every fare is limited to CAD 45–1,500 and rounded to two decimal places, both in `Flight.calculate_price` and in the vectorized batch calculation.

## Course concepts used

- Modularity & Functions: Reusable helper functions (`require_integer`, `update_db_seats`, `load_flights_db`) organize validation and database access.
- A `Flight` class: validates its inputs, computes `load_factor` and price, updates seats, and converts itself to a dictionary with `to_dict()`.
- Dictionaries and loops: validating and inserting CSV records one at a time through the `Flight` class.
- SQLite: an explicit `CREATE TABLE` schema, a `cursor` object, and parameterized `INSERT`/`SELECT`/`UPDATE`/`DELETE` with explicit `commit()`/`close()` — no SQL strings built from input.
- Pandas/NumPy: `np.select`, whole-column arithmetic, and `np.clip` price every flight in the table at once, instead of a Python loop.
- Assertions: input checks (uniqueness, valid ranges, missing values) on the whole table, plus fare-bound checks after pricing.

## Validation and edge cases

- Capacity and remaining seats must be whole numbers; fractional, boolean, and non-finite inputs are rejected before conversion. Seat changes must be whole numbers, and ticket quantities must be positive.
- The `Flight` constructor rejects non-positive capacity, out-of-range seats, non-positive fares, and non-positive demand/seasonal factors (see the rejected-flight demo).
- `update_seats` rejects a change that would take seats outside `0..capacity`.
- `update_db_seats` rejects an unknown flight ID and prevents the database from storing a remaining-seat value outside `0..capacity`.
- The batch-pricing table is checked for missing values, unique flight IDs, valid ranges, and positive factors before any price is calculated.
- Already-departed flights (relative to the fixed quote date) are excluded from pricing and printed.
- Sold-out flights are excluded from ranked results, and selling a seat on one is explicitly rejected.
- Interactive bookings parse quantities with `int()` and handle conversion errors, including superscript digits such as `²`. They reject non-positive or excessive quantities. The sale transaction also checks current inventory before committing.
- Every computed fare, single-flight and batch, is asserted to fall within CAD 45–1,500.

## Limitations

The dataset is fictional. Pricing multipliers are transparent teaching assumptions, not estimates fitted to real demand. The model does not optimize revenue or simulate real bookings. The quote date is fixed (2026-09-19) so results are reproducible; change it in the "Prepare dates and check the table" cell to see different flights included or excluded. This is a single-user notebook with no authentication, GUI, or deployment - all out of scope per the assignment. No LLM/API enhancement is included.

## Regression tests

From this folder, using the same Python environment as the notebook:

```bash
python -m unittest discover -s tests -v
```

The tests execute all notebook code cells in temporary working directories with real SQLite databases. They cover repeated Run All, stale-inventory sales, failed-reset rollback, integer validation, interactive booking, sold-out flights, manual reset, and pricing consistency. They do not write to the project database. Notebook outputs are cleared after source edits; run the notebook to regenerate current results.
