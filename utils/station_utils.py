import re


def extract_station_name(text: str) -> str:
    # Preserves the behavior expected by the original automation.
    # If your existing utils.extract_station_name has custom logic,
    # replace this implementation with that function.
    text = re.sub(r"\s+", " ", text or "").strip()
    return text
