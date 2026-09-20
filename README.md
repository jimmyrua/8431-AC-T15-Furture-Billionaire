# Potter Airlines Dynamic Pricing Project

RSM8431 — Team 15

This Python project prices Potter Airlines flights dynamically based on explainable business signals: time to departure, remaining capacity, route demand, and seasonality. It is a coursework project using fictional flight data and explainable pricing rules.

## Purpose

Two passengers booking the same flight can see different fares because they book at different times, remaining capacity has changed, or demand for the route differs. This project shows how a small set of transparent factors produces that behaviour, using a `Flight` class, SQLite persistence, and vectorized Pandas/NumPy calculations across the whole flight table.

## Files

| File | Purpose |
| --- | --- |
| `potter_airlines.ipynb` | Complete notebook: `Flight` class and single-flight demo, SQLite persistence, and vectorized batch pricing/search/update. |
| `potter_airlines.db` | SQLite database created and rebuilt by the notebook. |
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
5. Restart the kernel and run all cells from top to bottom. Every cell runs cleanly in sequence; the SQLite section rebuilds `potter_airlines.db` from the CSV each run, so results are reproducible.

No external API, LLM service, or API key is needed to run this notebook.

## Workflow

1. **Single-flight pricing (`Flight` class).** Demonstrates the pricing formula, a seat update, and input validation on one hand-built flight.
2. **SQLite persistence.** Loads `flights.csv`, validates each row through the `Flight` class, and inserts it (`Flight` → `to_dict()` → parameterized `INSERT`) into a `flights` table created with an explicit schema, using a `cursor` object and explicit `commit()`/`close()` calls. Demonstrates parameterized `SELECT`, `UPDATE`, and `DELETE` on a temporary test row, then reads the table back into a DataFrame.
3. **Batch pricing (vectorized).** Converts `departure_date` to real dates, computes `days_until_departure`, checks the whole table's assumptions with `assert`, excludes already-departed flights, and prices every remaining flight at once using `np.select`, whole-column arithmetic, and `np.clip` — no `for` loop over flights. A cross-check confirms the vectorized price agrees with `Flight.calculate_price` for the same flight.
4. **Filter and rank.** Excludes sold-out flights and ranks the rest by price.
5. **Operational update.** Sells 10 seats on a real flight (PA1002), saves the new seat count with a parameterized `UPDATE`, and shows the resulting fare increase.
6. **Edge case.** Attempts to sell a seat on the already sold-out PA1007 and shows it is rejected.

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

- Functions: `get_time_factor`.
- A `Flight` class: validates its inputs, computes `load_factor` and price, updates seats, and converts itself to a dictionary with `to_dict()`.
- Dictionaries and loops: validating and inserting CSV records one at a time through the `Flight` class.
- SQLite: an explicit `CREATE TABLE` schema, a `cursor` object, and parameterized `INSERT`/`SELECT`/`UPDATE`/`DELETE` with explicit `commit()`/`close()` — no SQL strings built from input.
- Pandas/NumPy: `np.select`, whole-column arithmetic, and `np.clip` price every flight in the table at once, instead of a Python loop.
- Assertions: input checks (uniqueness, valid ranges, missing values) on the whole table, plus fare-bound checks after pricing.

## Validation and edge cases

- The `Flight` constructor rejects non-positive capacity, out-of-range seats, non-positive fares, and non-positive demand/seasonal factors (see the rejected-flight demo).
- `update_seats` rejects a change that would take seats outside `0..capacity`.
- The batch-pricing table is checked for missing values, unique flight IDs, valid ranges, and positive factors before any price is calculated.
- Already-departed flights (relative to the fixed quote date) are excluded from pricing and printed.
- Sold-out flights are excluded from ranked results, and selling a seat on one is explicitly rejected.
- Every computed fare, single-flight and batch, is asserted to fall within CAD 45–1,500.

## Limitations

The dataset is fictional. Pricing multipliers are transparent teaching assumptions, not estimates fitted to real demand. The model does not optimize revenue or simulate real bookings. The quote date is fixed (2026-09-19) so results are reproducible; change it in the "Prepare dates and check the table" cell to see different flights included or excluded. This is a single-user notebook with no authentication, GUI, or deployment - all out of scope per the assignment. No LLM/API enhancement is included.

## Remaining work

- Record the 4-5 minute demonstration: run the system, explain a pricing decision, walk through meaningful code, and show the checked edge case.
