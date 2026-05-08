"""Translate field names between platforms."""

FIELD_MAP = {
    "hubspot": {
        "firstname": "first_name", "lastname": "last_name",
        "email": "email", "phone": "phone",
        "hs_lead_status": "lead_status", "dealstage": "deal_stage",
        "amount": "deal_value", "closedate": "close_date",
    },
    "airtable": {
        "Name": "full_name", "Email": "email", "Phone": "phone",
        "Status": "lead_status", "Deal Stage": "deal_stage",
        "Contract Value": "deal_value",
    },
    "notion": {
        "Client Name": "full_name", "Email": "email",
        "Stage": "deal_stage", "Value": "deal_value",
    }
}


def to_canonical(platform: str, data: dict) -> dict:
    mapping = FIELD_MAP.get(platform, {})
    return {mapping.get(k, k): v for k, v in data.items()}


def from_canonical(platform: str, data: dict) -> dict:
    mapping = {v: k for k, v in FIELD_MAP.get(platform, {}).items()}
    return {mapping.get(k, k): v for k, v in data.items()}
