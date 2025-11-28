import re
from typing import List

from .ast import (
    SelectQuery,
    Condition,
    OptimizeRouteQuery,
    InspectQuery,
)


_WHITESPACE = re.compile(r"\s+")


def _normalize(s: str) -> str:
    return _WHITESPACE.sub(" ", s).strip()


def parse_query(query: str):
    """
    Very small parser that recognizes:
    - SELECT ... FROM ... WHERE ...
    - OPTIMIZE ROUTE "A" TO "B" ...
    - INSPECT FREQUENCY 3.42GHz
    - INSPECT DEVICE "0xA4C1"
    - INSPECT TOWER "T-01"
    """
    normalized = _normalize(query)

    if normalized.upper().startswith("SELECT "):
        return _parse_select(normalized)
    if normalized.upper().startswith("OPTIMIZE ROUTE "):
        return _parse_optimize(normalized)
    if normalized.upper().startswith("INSPECT "):
        return _parse_inspect(normalized)

    raise ValueError(f"Unsupported N-SQL query: {query!r}")


def _parse_select(s: str) -> SelectQuery:
    # SELECT fields FROM table [WHERE ...]
    upper = s.upper()
    if " FROM " not in upper:
        raise ValueError("SELECT query missing FROM clause")

    select_part, rest = s.split(" FROM ", 1)
    fields_str = select_part[len("SELECT "):].strip()
    fields = [f.strip() for f in fields_str.split(",") if f.strip()]

    if " WHERE " in rest.upper():
        table_part, where_part = _split_case_insensitive(rest, " WHERE ")
        table = table_part.strip()
        conditions = _parse_conditions(where_part)
    else:
        table = rest.strip().rstrip(";")
        conditions = []

    return SelectQuery(fields=fields, table=table, conditions=conditions)


def _parse_conditions(s: str) -> List[Condition]:
    # simple "AND"-joined conditions
    parts = _split_all_case_insensitive(s, " AND ")
    conditions: List[Condition] = []

    for part in parts:
        part = part.strip().rstrip(";")
        if not part:
            continue

        m = re.search(r"\s+MATCHES\s+", part, flags=re.IGNORECASE)
        if m:
            field = part[:m.start()].strip()
            value = part[m.end():].strip()
            value = _strip_quotes(value)
            conditions.append(Condition(field=field, op="MATCHES", value=value))
            continue

        for op in ["<=", ">=", "!=", "=", "<", ">"]:
            idx = part.find(op)
            if idx != -1:
                field = part[:idx].strip()
                value = part[idx + len(op):].strip()
                value = _strip_quotes_or_number(value)
                conditions.append(Condition(field=field, op=op, value=value))
                break
        else:
            raise ValueError(f"Unrecognized condition: {part!r}")

    return conditions


def _parse_optimize(s: str) -> OptimizeRouteQuery:
    # OPTIMIZE ROUTE "A" TO "B" [PREFER ...] [MINIMIZE ... | MAXIMIZE ...]
    upper = s.upper()

    # "OPTIMIZE ROUTE "
    body = s[len("OPTIMIZE ROUTE "):]

    # Extract "FROM" device
    if not body.startswith('"'):
        raise ValueError("Expected quoted device for FROM")
    end_quote = body.find('"', 1)
    device_from = body[1:end_quote]
    remainder = body[end_quote + 1:].strip()

    if not remainder.upper().startswith("TO "):
        raise ValueError("Expected 'TO' in OPTIMIZE ROUTE")
    remainder = remainder[3:].strip()  # skip "TO "

    if not remainder.startswith('"'):
        raise ValueError("Expected quoted device for TO")
    end_quote = remainder.find('"', 1)
    device_to = remainder[1:end_quote]
    remainder = remainder[end_quote + 1:].strip().rstrip(";")

    preferences = {}
    goal = None

    # Optional PREFER
    prefer_idx = _find_case_insensitive(remainder, "PREFER ")
    if prefer_idx != -1:
        prefer_str = remainder[prefer_idx + len("PREFER "):]
        # maybe there's a MINIMIZE / MAXIMIZE after
        min_idx = _find_case_insensitive(prefer_str, "MINIMIZE ")
        max_idx = _find_case_insensitive(prefer_str, "MAXIMIZE ")

        if min_idx != -1 or max_idx != -1:
            split_idx = min(x for x in [min_idx, max_idx] if x != -1)
            prefer_block = prefer_str[:split_idx].strip()
            goal_block = prefer_str[split_idx:].strip()
        else:
            prefer_block = prefer_str.strip()
            goal_block = ""

        if "=" in prefer_block:
            key, val = prefer_block.split("=", 1)
            preferences[key.strip()] = _strip_quotes_or_number(val.strip())
    else:
        goal_block = remainder

    # MINIMIZE or MAXIMIZE
    if "MINIMIZE " in goal_block.upper():
        _, field = _split_case_insensitive(goal_block, "MINIMIZE ")
        goal = {"type": "MINIMIZE", "field": field.strip().rstrip(";")}
    elif "MAXIMIZE " in goal_block.upper():
        _, field = _split_case_insensitive(goal_block, "MAXIMIZE ")
        goal = {"type": "MAXIMIZE", "field": field.strip().rstrip(";")}

    return OptimizeRouteQuery(
        device_from=device_from,
        device_to=device_to,
        preferences=preferences,
        goal=goal,
    )


def _parse_inspect(s: str) -> InspectQuery:
    # INSPECT FREQUENCY 3.42GHz
    # INSPECT DEVICE "0xA4C1"
    # INSPECT TOWER "T-01"
    body = s[len("INSPECT "):].strip()
    parts = body.split(" ", 1)
    if len(parts) != 2:
        raise ValueError("Invalid INSPECT query")

    target_type = parts[0].upper()
    raw_val = parts[1].strip().rstrip(";")

    if target_type == "FREQUENCY":
        # naive: float+unit
        return InspectQuery(target_type="FREQUENCY", value=raw_val)
    elif target_type in ("DEVICE", "TOWER"):
        return InspectQuery(target_type=target_type, value=_strip_quotes(raw_val))

    raise ValueError(f"Unknown INSPECT target type: {target_type}")


def _strip_quotes(val: str) -> str:
    val = val.strip()
    if val.startswith('"') and val.endswith('"'):
        return val[1:-1]
    return val


def _strip_quotes_or_number(val: str):
    val = val.strip()
    if val.startswith('"') and val.endswith('"'):
        return val[1:-1]
    try:
        if "." in val:
            return float(val)
        return int(val)
    except ValueError:
        return val


def _split_case_insensitive(s: str, token: str):
    idx = s.upper().find(token.upper())
    if idx == -1:
        return s, ""
    return s[:idx], s[idx + len(token):]


def _split_all_case_insensitive(s: str, token: str):
    parts = []
    token_upper = token.upper()
    remaining = s
    while True:
        idx = remaining.upper().find(token_upper)
        if idx == -1:
            parts.append(remaining)
            break
        parts.append(remaining[:idx])
        remaining = remaining[idx + len(token):]
    return parts


def _find_case_insensitive(s: str, token: str) -> int:
    return s.upper().find(token.upper())
