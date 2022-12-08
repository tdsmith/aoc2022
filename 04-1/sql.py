import pprint
from pathlib import Path

import duckdb
import typer

schema = """
CREATE TABLE assignments (
    row VARCHAR
);
"""

query = Path("sql.sql").read_text()


def main(file: Path):
    conn = duckdb.connect(":memory:")
    conn.execute(schema)
    conn.execute(f"COPY assignments FROM '{file}' (DELIMITER '')")
    conn.execute(query)
    pprint.pprint(conn.fetchall())


if __name__ == "__main__":
    typer.run(main)
