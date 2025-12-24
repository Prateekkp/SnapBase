def build_prompt(question, schema):
    if schema:
        schema_text = "\n".join(
            f"{t}.{c} ({d})" for t, c, d in schema
        )
    else:
        schema_text = "No schema information available"

    return f"""
You are an expert MYSQL assistant.

SCHEMA:
{schema_text}

RULES:
- Generate a SINGLE SQL query (not multiple queries)
- Only generate SQL queries
- No DELETE, DROP, UPDATE, ALTER, CREATE, TRUNCATE statements
- Use only the tables and columns from the given schema
- If schema is available, use the exact table and column names
- Generate valid MySQL syntax
- For "describe tables" requests, use SELECT from information_schema or SHOW TABLES

QUESTION:
{question}

SQL:
"""