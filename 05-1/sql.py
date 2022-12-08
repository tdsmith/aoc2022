import pprint
from pathlib import Path

import duckdb
import typer

schema = """
CREATE TABLE input (
    line VARCHAR
);
"""

query = Path("sql.sql").read_text()


def main(file: Path):
    conn = duckdb.connect(":memory:")
    conn.execute(schema)
    conn.execute(f"COPY input FROM '{file}' (DELIMITER '')")
    conn.execute(query)
    pprint.pprint(conn.fetchall())


if __name__ == "__main__":
    typer.run(main)
