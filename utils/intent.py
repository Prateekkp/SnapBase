def is_direct_sql(text: str) -> bool:
    text = text.strip().lower()
    
    # For DESCRIBE/DESC - only valid if followed by a single table name
    if text.startswith("describe ") or text.startswith("desc "):
        parts = text.split()
        if len(parts) == 2 and parts[1] not in ("all", "the", "tables", "database", "databases", "me"):
            return True
        return False
    
    # For SHOW - only valid if it's SHOW TABLES, SHOW DATABASES, SHOW COLUMNS, etc.
    # Not "show me all tables" or similar natural language
    if text.startswith("show "):
        parts = text.split()
        valid_show_keywords = ("tables", "databases", "columns", "schemas", "engines", "status", "variables")
        if len(parts) >= 2 and parts[1] in valid_show_keywords:
            return True
        # Check if it has natural language words that indicate it's not SQL
        natural_language_words = ("me", "all", "list", "give", "tell", "what", "which", "find")
        if any(word in parts for word in natural_language_words):
            return False
        return False
    
    # For SELECT, INSERT, UPDATE, DELETE, CREATE, DROP - these are usually direct SQL
    sql_keywords = ("select ", "insert ", "update ", "delete ", "create ", "drop ")
    for keyword in sql_keywords:
        if text.startswith(keyword):
            return True
    
    return False
