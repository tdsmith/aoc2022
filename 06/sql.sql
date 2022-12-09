WITH kmers AS (
    SELECT
        line_no,
        end_pos,
        line[end_pos-({k}-1):end_pos] AS kmer
    FROM (
        SELECT
            rowid AS line_no,
            line,
            UNNEST(generate_series({k}, strlen(line))) AS end_pos
        FROM input
    )
)

, d_count AS (
    SELECT
        line_no,
        end_pos,
        COUNT(DISTINCT k) AS n
    FROM
        (SELECT line_no, end_pos, UNNEST(string_split(kmer, '')) AS k FROM kmers)
    GROUP BY
        line_no,
        end_pos
)

SELECT MIN(end_pos)
FROM d_count
WHERE n = {k}
GROUP BY line_no
