"""CRM Sync Engine — FastAPI webhook receiver."""
from fastapi import FastAPI, Request, BackgroundTasks
from sync.conflict_resolver import resolve
from sync.field_mapper import to_canonical, from_canonical
import httpx, os, json, logging

app = FastAPI(title="CRM Sync Engine")
log = logging.getLogger("sync")


@app.post("/webhooks/hubspot")
async def hubspot_webhook(req: Request, bg: BackgroundTasks):
    payload = await req.json()
    bg.add_task(handle_change, "hubspot", payload)
    return {"status": "queued"}


@app.post("/webhooks/airtable")
async def airtable_webhook(req: Request, bg: BackgroundTasks):
    payload = await req.json()
    bg.add_task(handle_change, "airtable", payload)
    return {"status": "queued"}


@app.post("/webhooks/notion")
async def notion_webhook(req: Request, bg: BackgroundTasks):
    payload = await req.json()
    bg.add_task(handle_change, "notion", payload)
    return {"status": "queued"}


async def handle_change(source: str, payload: dict):
    """Process a change from one platform and sync to others."""
    canonical = to_canonical(source, payload)
    targets = ["hubspot", "airtable", "notion"]
    targets.remove(source)

    for target in targets:
        resolved = resolve(source, target, canonical)
        if resolved:
            target_data = from_canonical(target, resolved)
            await push_to_platform(target, target_data)
            log.info(f"Synced {source} → {target}: {canonical.get('id')}")


async def push_to_platform(platform: str, data: dict):
    """Push resolved data to target platform."""
    # Platform-specific API calls
    pass
