import re

def extract_sql(text: str) -> str | None:
    if not text:
        return None

    # Case 1: SQL inside ```sql blocks
    match = re.search(r"```sql\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Case 2: Starts directly with safe SQL keyword (READ-ONLY)
    text = text.strip()
    # ✋ SECURITY: Only allow safe, read-only SQL keywords
    safe_keywords = ("select", "show", "describe", "desc", "explain", "with")
    for kw in safe_keywords:
        if text.lower().startswith(kw):
            return text

    return None
