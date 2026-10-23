from data.pan_records import PAN_RECORDS
import re

PAN_PATTERN = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")


def normalize_pan(pan: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", pan or "").upper()


def validate_pan(pan: str) -> bool:
    value = normalize_pan(pan)
    if len(value) != 10:
        return False
    if not PAN_PATTERN.match(value):
        return False

    # Use a lightweight sanity check: first five chars must be alpha, next four numeric, last must be alpha.
    return value[:5].isalpha() and value[5:9].isdigit() and value[9].isalpha()


def lookup_pan_record(pan: str):
    return PAN_RECORDS.get(normalize_pan(pan))


def build_fill_payload(record: dict) -> dict:
    return {
        "full_name": record.get("full_name", ""),
        "father_name": record.get("father_name", ""),
        "date_of_birth": record.get("date_of_birth", ""),
        "address": record.get("address", ""),
        "city": record.get("city", ""),
        "state": record.get("state", ""),
        "pincode": record.get("pincode", ""),
        "email": record.get("email", ""),
        "mobile": record.get("mobile", ""),
    }
