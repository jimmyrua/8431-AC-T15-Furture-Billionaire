# Potter Airlines Dynamic Pricing Project

RSM8431 — Team 15

This Python project explores how flight fares can change with time to departure, seat availability, route demand, and seasonality. It is a coursework project using fictional flight data and explainable pricing rules.

The project is in development. This README describes the code currently saved in the repository and the remaining work.

## Files

| File | Purpose |
| --- | --- |
| `potter_airlines.ipynb` | Main notebook containing pricing logic, a `Flight` class, and example checks. |
| `flights.csv` | Twenty fictional flights used as the input dataset. Fare amounts are interpreted as Canadian dollars (CAD). |
| `Potter_Airlines_Project_Specification.docx` | Assignment requirements. |
| `Potter_Airlines_Student_Rubric.docx` | Grading criteria. |

The CSV includes flight identifiers, origins, destinations, departure dates, base fares, total capacity, remaining seats, demand factors, and seasonal factors. It includes sold-out flights and flights with very few or all seats available.

## Setup and Run

1. Clone or download this repository.
2. Use a Python environment with Pandas and a Jupyter-compatible notebook runner. In VS Code, install the Python and Jupyter extensions and select your Python environment as the notebook kernel.
3. Install the packages in that environment if needed:

   ```bash
   python -m pip install pandas ipykernel
   ```

4. Open `potter_airlines.ipynb`. Keep `flights.csv` in the same folder and run the notebook with that folder as the working directory.
5. Restart the kernel and run all cells from top to bottom.

After changing the `Flight` class, rerun its definition and recreate any test objects before calling their methods. Repeated calls to `update_seats()` change the object's current state; recreate the object to reset it.

## Current Functionality

- Defines a time-factor function that rejects negative departure intervals.
- Defines a Flight class with identifiers, route, base fare, capacity, remaining seats, demand and seasonal factors.
- Checks initial capacity, seat range, positive base fares and positive factors.
- Calculates occupancy and bounded five-factor prices.
- Updates seats while rejecting invalid changes.
- Demonstrates a rejected seat update and a price increase from CAD 556.38 to CAD 561.33 after selling five seats at a constant 12-day interval.

The current example is manually created and is not yet connected to the CSV. Earlier CSV-loading, date-preparation and vectorized calculations are absent from the latest saved notebook.

All five saved code cells pass a clean sequential execution. The invalid-constructor example supplies route arguments and correctly catches the rejected seat count.

## Pricing Logic

The saved single-flight method uses:

```text
load_factor = 1 - seats_remaining / capacity
capacity_factor = 1 + 0.45 * load_factor
price = base_fare * time_factor * capacity_factor * demand_factor * seasonal_factor
```

| Days to departure | Time factor |
| --- | --- |
| 0–7 | 1.35 |
| 8–21 | 1.10 |
| More than 21 | 1.00 |

Higher occupancy increases the capacity factor. A shorter booking interval increases the time factor. The current method limits fares to CAD 45–1,500 and rounds the result to two decimal places.

Demand and seasonal factors are supplied when creating a Flight object. The CSV also contains these factors for future batch calculations.

## Remaining Work

- Restore CSV loading, date preparation and meaningful whole-column calculations.
- Extend validation to integer seat counts and missing/non-finite inputs.
- Connect departure dates and CSV records to the pricing workflow.
- Calculate prices across the full dataset and filter or rank available flights.
- Add SQLite persistence with a clear schema and parameterized INSERT, SELECT, UPDATE, and DELETE operations.
- Add explicit fare assertions and finalize edge-case demonstrations.
- Finalize reproducible run instructions and prepare the 4–5 minute recorded demonstration.

## Limitations

The dataset is fictional. Pricing multipliers are transparent teaching assumptions rather than estimates fitted to real demand. The model does not optimize revenue or simulate actual bookings. A fixed pricing date is planned for reproducible batch comparisons.

SQLite storage, full batch pricing, complete validation, and the recorded demonstration are not yet included. The current saved example supplies departure intervals manually. No external API, LLM service, or API credentials are required for the current notebook.
