"""Conflict resolution rules between platforms."""

RESOLUTION_RULES = {
    "deal_stage":      "hubspot_wins",
    "deal_value":      "hubspot_wins",
    "close_date":      "hubspot_wins",
    "project_status":  "airtable_wins",
    "delivery_date":   "airtable_wins",
    "assigned_team":   "airtable_wins",
    "contract_value":  "flag_review",
    "default":         "last_write_wins",
}

SYNCING = set()  # Dedup — prevents A→B→A loops


def resolve(source: str, target: str, data: dict) -> dict | None:
    """Return resolved data to push to target, or None if skipped."""
    record_id = data.get("id")
    key = f"{record_id}:{source}:{target}"

    if key in SYNCING:
        return None  # Loop detected
    SYNCING.add(key)

    resolved = {}
    for field, value in data.items():
        rule = RESOLUTION_RULES.get(field, RESOLUTION_RULES["default"])
        if rule == f"{source}_wins":
            resolved[field] = value
        elif rule == f"{target}_wins":
            pass  # Target keeps its value
        elif rule == "flag_review":
            _flag_for_review(record_id, field, source, value)
        else:  # last_write_wins
            resolved[field] = value

    SYNCING.discard(key)
    return resolved or None


def _flag_for_review(record_id, field, source, value):
    print(f"[REVIEW REQUIRED] {record_id}.{field} changed in {source} → {value}")
