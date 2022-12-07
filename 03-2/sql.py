from pathlib import Path

import duckdb
import typer

schema = """
CREATE TABLE rucksacks (
    sack VARCHAR
);
"""

query = Path("sql.sql").read_text()


def main(file: Path):
    conn = duckdb.connect(":memory:")
    conn.execute(schema)
    conn.execute(f"COPY rucksacks FROM '{file}'")
    conn.execute(query)
    print(conn.fetchall())


if __name__ == "__main__":
    typer.run(main)
