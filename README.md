# PAN Autofill AI Agent

This project demonstrates a safe, privacy-first AI agent that fills application forms using only a PAN, with consent and validation guardrails.

## What it does

- Validates PAN format
- Requires explicit user consent
- Looks up a verified identity record for the PAN
- Maps the returned identity data into application form fields automatically
- Uses a deterministic field-mapping layer so the AI layer never becomes the source of truth

## Key safety principles

- Only a valid PAN is accepted
- Consent must be granted before any data lookup
- Records are mapped through an allowlist of supported fields only
- Unverified or missing records do not trigger autofill
- The system keeps the AI for parsing and mapping, not identity truth

## Tech stack

- FastAPI
- Jinja2 templates
- Vanilla JavaScript
- Python-based service layer

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Then open http://localhost:8000

## API examples

### Validate PAN

```bash
curl -X POST http://localhost:8000/api/validate-pan \
  -H "Content-Type: application/json" \
  -d '{"pan":"ABCDE1234F"}'
```

### Autofill using PAN

```bash
curl -X POST http://localhost:8000/api/autofill \
  -H "Content-Type: application/json" \
  -d '{"pan":"ABCDE1234F","consent":true}'
```

## Demo records

The repository includes a few sample PAN records for demonstration. In production, replace this with a verified KYC or government-authorized data source.
