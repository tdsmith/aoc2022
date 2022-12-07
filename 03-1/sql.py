from pathlib import Path

import duckdb
import typer

schema = """
CREATE TABLE rucksacks (
    sack VARCHAR
);
"""

query = """
WITH compartments AS (
    SELECT
        ROW_NUMBER() OVER () AS elf,
        string_to_array(left(sack, strlen(sack)/2), '') AS top,
        string_to_array(right(sack, strlen(sack)/2), '') AS bottom
    FROM rucksacks
)

, doubled_item AS (
    SELECT
        elf,
        UNNEST(top) item
    FROM compartments
    INTERSECT
    SELECT
        elf,
        UNNEST(bottom) item
    FROM compartments
)

, elfs AS (
    SELECT
        elf,
        CASE
            WHEN item < 'a' THEN ord(item) - ord('A') + 27
            ELSE ord(item) - ord('a') + 1
        END AS priority
    FROM doubled_item
)

SELECT sum(priority) FROM elfs
"""


def main(file: Path):
    conn = duckdb.connect(":memory:")
    conn.execute(schema)
    conn.execute(f"COPY rucksacks FROM '{file}'")
    conn.execute(query)
    print(conn.fetchone())


if __name__ == "__main__":
    typer.run(main)
