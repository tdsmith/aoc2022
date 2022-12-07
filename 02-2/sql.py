from pathlib import Path

import duckdb
import typer

schema = """
CREATE TABLE instructions (
    you VARCHAR,
    me VARCHAR
);
"""

query = """
WITH victory AS (
    SELECT *
    FROM (VALUES
        ('A', 'A', 3),
        ('A', 'B', 6),
        ('B', 'B', 3),
        ('B', 'C', 6),
        ('C', 'A', 6),
        ('C', 'C', 3),
    ) Victory(you, me, score)
)

, plays AS (
    SELECT *
    FROM (VALUES
        ('A', 'X', 'C'),
        ('A', 'Y', 'A'),
        ('A', 'Z', 'B'),
        ('B', 'X', 'A'),
        ('B', 'Y', 'B'),
        ('B', 'Z', 'C'),
        ('C', 'X', 'B'),
        ('C', 'Y', 'C'),
        ('C', 'Z', 'A'),
    ) Plays(you, instruction, move)
)

, play_value AS (
    SELECT *
    FROM (VALUES
        ('A', 1),
        ('B', 2),
        ('C', 3),
    ) PlayValue(me, score)
)

SELECT
    SUM(play_value.score) + SUM(victory.score)
FROM instructions
    LEFT JOIN plays
        ON instructions.you = plays.you
        AND instructions.me = plays.instruction
    LEFT JOIN victory
        ON instructions.you = victory.you
        AND plays.move = victory.me
    LEFT JOIN play_value
        ON plays.move = play_value.me
"""

def main(file: Path):
    conn = duckdb.connect(":memory:")
    conn.execute(schema)
    conn.execute(f"COPY instructions FROM '{file}' (DELIMITER ' ')")
    conn.execute(query)
    print(conn.fetchone())

if __name__ == "__main__":
    typer.run(main)
