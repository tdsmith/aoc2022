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
        ) AS completely_contained
    FROM pairs
)

SELECT SUM(CASE completely_contained WHEN TRUE THEN 1 ELSE 0 END)
FROM contained
