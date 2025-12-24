import re

def extract_sql(text: str) -> str | None:
    if not text:
        return None

    # Case 1: SQL inside ```sql blocks
    match = re.search(r"```sql\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Case 2: Starts directly with SQL keyword
    text = text.strip()
    for kw in ("select", "show", "describe", "desc", "explain"):
        if text.lower().startswith(kw):
            return text

    return None
