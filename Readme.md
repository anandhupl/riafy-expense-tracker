# Personal Expense Tracker

A lightweight, single-page personal expense tracker built to run locally with zero deployment overhead. 

## How to Run

1. Ensure you have Python 3.x installed.
2. Install the required dependency:
```bash
   pip install flask

```

3. Run the application:
```bash
   python app.py

```


4. Open your browser and navigate to: `http://127.0.0.1:5000`

## Stack Choices and Tradeoffs

* **Backend:** Python + Flask. Chosen for ultimate execution speed during development. It provides rapid API routing without the heavy boilerplate of larger frameworks like Django.
* **Database:** SQLite (via Python's built-in `sqlite3` module). Tradeoff: Not suitable for high-concurrency or multi-user network deployment, but absolutely perfect for a locally-run personal tool. It requires zero configuration or separate database servers.
* **Frontend:** Plain HTML, Vanilla JS (Fetch API), and Bootstrap 5 CDN. Tradeoff: Lacks the state-management elegance of React/Vue, meaning manual DOM updates are required. However, it entirely eliminates Node.js/NPM build steps and dependency bloat for a simple CRUD app.

## What's Done vs. Skipped

* **Done:** End-to-end CRUD functionality, real-time filtering (by search text, date range, and category), automated current-month summary aggregation, and input validation. Sorting is handled natively by the SQL query (`ORDER BY date DESC, id DESC`).
* **Skipped:** User authentication, multi-currency support, pagination (all records load in one scrollable table), and heavy frontend frameworks. These were deprioritized to ruthlessly execute on the core logical requirements within the time limit.

## Edge Cases Handled

* **Empty States:** The UI clearly indicates when no expenses match the active filters or when the monthly summary is zero.
* **Invalid Inputs:** HTML5 form constraints prevent empty titles, unselected categories, and negative/zero amounts. The backend strips whitespace to prevent blank submissions. Added a logical check to prevent paradoxical date filtering (Start Date > End Date).
* **String Sanitization:** Handled Javascript string escaping for UI data attributes to prevent XSS injection, and applied CSS text-breaking to prevent massive strings without spaces from destroying the table layout.