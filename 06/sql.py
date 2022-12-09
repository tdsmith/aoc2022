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
    conn.execute(query.format(k=4))
    pprint.pprint(conn.fetchall())
    conn.execute(query.format(k=14))
    pprint.pprint(conn.fetchall())


if __name__ == "__main__":
    typer.run(main)
