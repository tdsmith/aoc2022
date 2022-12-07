import duckdb
import typer

schema = """
CREATE TABLE moves (
    you VARCHAR,
    me VARCHAR
);
"""

query = """
WITH victory AS (
    SELECT *
    FROM (VALUES
        ('A', 'X', 3),
        ('A', 'Y', 6),
        ('B', 'Y', 3),
        ('B', 'Z', 6),
        ('C', 'X', 6),
        ('C', 'Z', 3),
    ) Victory(you, me, score)
)

, play_value AS (
    SELECT *
    FROM (VALUES
        ('X', 1),
        ('Y', 2),
        ('Z', 3),
    ) PlayValue(me, score)
)

SELECT
    SUM(play_value.score) + SUM(victory.score)
FROM moves
    LEFT JOIN victory USING (you, me)
    LEFT JOIN play_value USING (me)
"""

def main(file: typer.FileText):
    moves = [line.strip().split() for line in file]

    conn = duckdb.connect(":memory:")
    conn.execute(schema)
    conn.executemany("INSERT INTO moves VALUES (?, ?)", moves)
    conn.execute(query)
    print(conn.fetchall())

if __name__ == "__main__":
    typer.run(main)
