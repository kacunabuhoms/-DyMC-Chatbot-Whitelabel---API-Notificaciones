from typing import Any


def flatten(data: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            result.update(flatten(value, full_key))
        elif not isinstance(value, list):
            result[full_key] = value
    return result


def expand_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    base = flatten({k: v for k, v in data.items() if not isinstance(v, list)})
    lists = {k: v for k, v in data.items() if isinstance(v, list)}

    if not lists:
        return [base]

    rows: list[dict[str, Any]] = []
    for list_key, items in lists.items():
        for item in items:
            row = dict(base)
            if isinstance(item, dict):
                row.update(flatten(item, list_key))
            else:
                row[list_key] = item
            rows.append(row)

    return rows if rows else [base]
