<div align="center">

## 🔗 CRM Sync Engine

Real-time bidirectional sync across **HubSpot · Airtable · Notion**

*One source of truth. Always.*

</div>

---

The problem: your sales team lives in HubSpot, ops team in Airtable, leadership in Notion. Within hours they diverge. Reconciliation takes hours every week.

This FastAPI service sits between all three, listens for webhooks, and keeps every platform in sync within seconds.

---

### Architecture

```
HubSpot  ──webhook──►┐
Airtable ──webhook──►│  Sync Engine (FastAPI)
Notion   ──webhook──►│  ├── Conflict resolver
                     │  ├── Dedup / loop prevention
                     │  ├── Retry queue (Redis)
                     │  └── Audit log (Postgres)
                     │
                     ├──API write──► HubSpot
                     ├──API write──► Airtable
                     └──API write──► Notion
```

### Conflict Resolution

```python
RULES = {
    "deal_stage":    "hubspot_wins",   # Sales owns pipeline
    "project_status": "airtable_wins", # Ops owns delivery
    "contract_value": "flag_review",   # Human review required
    "default":       "last_write_wins"
}
```

### Files

```
crm-sync-engine/
├── main.py                    # FastAPI app
├── sync/
│   ├── conflict_resolver.py   # Resolution rules
│   └── field_mapper.py        # Field name translation
├── config/
│   └── field_mapping.json     # Platform field map
└── requirements.txt
```

### Run

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
redis-server &
```

Configure webhooks to point to:
- `POST /webhooks/hubspot`
- `POST /webhooks/airtable`
- `POST /webhooks/notion`

---

<sub>[@rohan643](https://github.com/rohan643)</sub>
