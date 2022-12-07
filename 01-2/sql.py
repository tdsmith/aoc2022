import duckdb
import typer

schema = """
CREATE TABLE items (
    calories INTEGER
);
"""

query = """
WITH indexed AS (
    SELECT
        CASE
            WHEN calories IS NULL THEN row_number() OVER ()
            ELSE NULL
        END AS elf,
        calories
    FROM items
)

, elf_fill AS (
    SELECT
        MIN(elf) OVER (ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING) AS elf,
        calories
    FROM indexed
)

SELECT
    SUM(calories) AS sum_calories
FROM elf_fill
GROUP BY elf
ORDER BY sum_calories DESC
LIMIT 3
"""

def main(file: typer.FileText):
    calories = [(int(i),) if i.strip() else (None,) for i in file.readlines()]

    conn = duckdb.connect(":memory:")
    conn.execute(schema)
    conn.executemany("INSERT INTO items VALUES (?)", calories)
    conn.execute(query)
    print(conn.fetchall())

if __name__ == "__main__":
    typer.run(main)
