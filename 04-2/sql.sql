WITH pairs AS (
    SELECT
        arr[1][1]::INTEGER AS left1,
        arr[1][2]::INTEGER AS right1,
        arr[2][1]::INTEGER AS left2,
        arr[2][2]::INTEGER AS right2
    FROM (
        SELECT
            list_transform(
                str_split("row", ','),
                x -> str_split(x, '-')
            ) AS arr
        FROM assignments
    )
)

, contained AS (
    SELECT
        (
            -- 1 contains 2
            (left1 <= left2 AND right2 <= right1) OR
            -- the converse
            (left2 <= left1 AND right1 <= right2)
        ) AS completely_contained,
        NOT (
            right1 < left2 OR right2 < left1
        ) AS overlap,
    FROM pairs
)

SELECT
    SUM(completely_contained::INTEGER),
    SUM(overlap::INTEGER)
FROM contained
