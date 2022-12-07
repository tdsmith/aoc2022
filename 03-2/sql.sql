WITH compartments AS (
    SELECT
        (ROW_NUMBER() OVER () - 1) / 3 AS group,
        (ROW_NUMBER() OVER () - 1) % 3 AS idx,
        string_to_array(sack, '') AS items
    FROM rucksacks
)

, pivot AS (
    SELECT
        first(items) FILTER (WHERE idx = 0) AS elf1,
        first(items) FILTER (WHERE idx = 1) AS elf2,
        first(items) FILTER (WHERE idx = 2) AS elf3
    FROM compartments
    GROUP BY "group"
)

, shared_item AS (
    SELECT
        array_filter(
            elf1,
            item -> array_has(elf2, item) AND array_has(elf3, item)
        )[1] AS item
    FROM pivot
)

, priorities AS (
    SELECT
        CASE
            WHEN item < 'a' THEN ord(item) - ord('A') + 27
            ELSE ord(item) - ord('a') + 1
        END AS priority
    FROM shared_item
)

SELECT sum(priority) FROM priorities
