import sqlite3
from pathlib import Path

from fastmcp import FastMCP

mcp = FastMCP(name="Expense Tracker", instructions="A simple expense tracker tool.")
DB_PATH = Path(__file__).resolve().parents[2] / "expense_tracker.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
       CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            subcategory TEXT,
            description TEXT
            )
        """
    )
    conn.commit()
    conn.close()

@mcp.tool()
def add_expense(
    date: str,
    category: str,
    amount: float,
    subcategory: str | None = None,
    description: str | None = None,
) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO expenses (date, category, amount, subcategory, description)
        VALUES (?, ?, ?, ?, ?)
        """,
        (date, category, amount, subcategory, description),
    )
    conn.commit()
    conn.close()

@mcp.tool()
def list_expenses() -> list[tuple]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    conn.close()
    return expenses

@mcp.tool()
def summarize_expenses_by_category() -> list[tuple]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT category, SUM(amount) as total_amount
        FROM expenses
        GROUP BY category
        """
    )
    summary = cursor.fetchall()
    conn.close()
    return summary

@mcp.tool()
def edit_expense(
    expense_id: int,
    date: str,
    category: str,
    amount: float,
    subcategory: str | None = None,
    description: str | None = None,
) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE expenses
        SET date = ?, category = ?, amount = ?, subcategory = ?, description = ?
        WHERE id = ?
        """,
        (date, category, amount, subcategory, description, expense_id),
    )
    conn.commit()
    conn.close()

@mcp.tool()
def delete_expense(expense_id: int) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()



def main():
    init_db()
    mcp.run(transport="http", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()


