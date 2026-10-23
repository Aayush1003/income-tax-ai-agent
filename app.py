from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from services.pan_service import normalize_pan, validate_pan, lookup_pan_record, build_fill_payload

app = FastAPI(
    title="PAN Autofill AI Agent",
    description="A lightweight AI-assisted PAN-based identity autofill agent",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class PanRequest(BaseModel):
    pan: str = Field(..., min_length=10, max_length=10, description="PAN number")


class AutofillRequest(PanRequest):
    consent: bool = Field(False, description="Consent to fetch verified identity details")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/validate-pan")
def validate_pan_endpoint(payload: PanRequest):
    normalized = normalize_pan(payload.pan)
    is_valid = validate_pan(normalized)
    return {
        "valid": is_valid,
        "normalized_pan": normalized,
        "message": "PAN looks valid." if is_valid else "PAN format is invalid.",
    }


@app.post("/api/autofill")
def autofill_endpoint(payload: AutofillRequest):
    normalized = normalize_pan(payload.pan)
    if not validate_pan(normalized):
        raise HTTPException(status_code=400, detail="Invalid PAN format")

    if not payload.consent:
        raise HTTPException(status_code=403, detail="User consent is required before fetching identity data")

    record = lookup_pan_record(normalized)
    if record is None:
        return {
            "success": False,
            "source_verified": False,
            "message": "PAN is valid but no verified profile was found for this record.",
            "fields": {},
        }

    return {
        "success": True,
        "source_verified": True,
        "message": "Verified profile retrieved successfully.",
        "fields": build_fill_payload(record),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
