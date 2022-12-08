CREATE MACRO process(stacks, n, source, dest) AS (
    -- unpack the (doubly-nested) stacks list to a table
    WITH unpacked AS (SELECT generate_subscripts(stacks, 1) AS idx, UNNEST(stacks) AS stack)

    -- perform the transfer operation
    , transfer AS (
        SELECT
            idx,
            CASE
                WHEN idx = source THEN stack[1:len(stack)-n]
                WHEN idx = dest THEN list_cat(stack, stacks[source][len(stacks[source])-n+1:])
                ELSE stack
            END AS stack
        FROM unpacked
    )

    -- repack the stacks list
    SELECT list(transfer.stack ORDER BY idx) FROM transfer
);

-- Only `applied` is actually recursive but we need to declare it here
WITH RECURSIVE container_grid AS (  -- Parse the stacks, part 1
    SELECT
        rowid,
        generate_subscripts(line, 1) AS col,
        UNNEST(line) AS ch,
    FROM (
        SELECT rowid, string_split(line, '') AS line
        FROM input
        WHERE line LIKE '%[%'
    )
)

, containers AS (
    SELECT
        (col - 1) / 4 + 1 AS stack,
        array_agg(ch ORDER BY rowid DESC) AS labels
    FROM (
        SELECT *, LAG(ch) OVER (PARTITION BY rowid ORDER BY col ASC) "last"
        FROM container_grid
    )
    WHERE "last" = '['
    GROUP BY stack
    ORDER BY stack
)

-- Command parsing
, commands AS (
    SELECT
        ROW_NUMBER() OVER () AS idx,
        regexp_extract(line, 'move (\d+) from', 1)::INTEGER AS n,
        regexp_extract(line, 'from (\d+) to', 1)::INTEGER AS source,
        regexp_extract(line, 'to (\d+)', 1)::INTEGER AS dest
    FROM input
    WHERE line LIKE 'move%'
)

-- Iterate over the list of commands
, applied AS (
    SELECT
        1 AS next_idx,
        list(labels ORDER BY stack) AS stacks
    FROM containers
    UNION ALL
    SELECT
        applied.next_idx + 1 AS next_idx,
        process(stacks, n, source, dest) AS stacks
    FROM
        applied
        INNER JOIN commands ON applied.next_idx = commands.idx
)

SELECT
    replace(
        list_string_agg(
            -- extract the item at the top of each stack
            list_transform(stacks, stack -> stack[len(stack)])
        ),
        ',',
        ''
    )
FROM applied
ORDER BY next_idx DESC
LIMIT 1;
