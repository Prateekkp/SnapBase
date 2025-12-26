"""
SQL Query Validator - Protects database from destructive operations
Blocks all data manipulation and schema modification commands
"""

import re
from typing import Tuple


# Comprehensive list of dangerous SQL keywords and patterns
DESTRUCTIVE_KEYWORDS = {
    # Data Modification Language (DML)
    'DELETE', 'INSERT', 'UPDATE', 'REPLACE', 'MERGE', 'UPSERT',
    
    # Data Definition Language (DDL)
    'DROP', 'CREATE', 'ALTER', 'TRUNCATE', 'RENAME',
    
    # Data Control Language (DCL)
    'GRANT', 'REVOKE',
    
    # Transaction Control
    'COMMIT', 'ROLLBACK', 'SAVEPOINT',
    
    # Administrative Commands
    'SET', 'RESET', 'SHUTDOWN', 'KILL',
    
    # Database/Table Management
    'USE', 'LOAD', 'IMPORT', 'EXPORT',
    
    # Index Operations
    'REINDEX', 'ANALYZE', 'VACUUM', 'OPTIMIZE',
    
    # Other dangerous operations
    'CALL', 'EXECUTE', 'EXEC', 'PREPARE',
}

# Read-only keywords that are safe to execute
SAFE_KEYWORDS = {
    'SELECT', 'SHOW', 'DESCRIBE', 'DESC', 'EXPLAIN', 'WITH'
}


def normalize_sql(sql: str) -> str:
    """
    Normalize SQL query by removing comments and extra whitespace
    
    Args:
        sql: Raw SQL query string
        
    Returns:
        Normalized SQL string
    """
    # Remove single-line comments (-- style)
    sql = re.sub(r'--[^\n]*', '', sql)
    
    # Remove multi-line comments (/* */ style)
    sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)
    
    # Remove extra whitespace
    sql = ' '.join(sql.split())
    
    return sql.strip()


def extract_first_keyword(sql: str) -> str:
    """
    Extract the first SQL keyword from a query
    
    Args:
        sql: SQL query string
        
    Returns:
        First keyword in uppercase, or empty string
    """
    sql = normalize_sql(sql)
    
    # Match first word (keyword)
    match = re.match(r'^\s*([A-Za-z]+)', sql)
    if match:
        return match.group(1).upper()
    
    return ""


def contains_destructive_keywords(sql: str) -> Tuple[bool, str]:
    """
    Check if SQL contains any destructive keywords
    
    Args:
        sql: SQL query string
        
    Returns:
        Tuple of (is_destructive, detected_keyword)
    """
    sql = normalize_sql(sql)
    sql_upper = sql.upper()
    
    # Check for destructive keywords anywhere in the query
    for keyword in DESTRUCTIVE_KEYWORDS:
        # Use word boundaries to avoid false positives
        pattern = r'\b' + keyword + r'\b'
        if re.search(pattern, sql_upper):
            return True, keyword
    
    return False, ""


def is_safe_query(sql: str) -> Tuple[bool, str]:
    """
    Validate if a SQL query is safe to execute (read-only)
    
    Args:
        sql: SQL query string
        
    Returns:
        Tuple of (is_safe, error_message)
        - is_safe: True if query is safe, False otherwise
        - error_message: Description of why query is unsafe (empty if safe)
    """
    if not sql or not sql.strip():
        return False, "Empty query"
    
    sql = normalize_sql(sql)
    
    # Check first keyword
    first_keyword = extract_first_keyword(sql)
    
    if not first_keyword:
        return False, "Could not parse SQL query"
    
    # Check if first keyword is safe
    if first_keyword not in SAFE_KEYWORDS:
        return False, f"Query starts with forbidden keyword: {first_keyword}"
    
    # Check for destructive keywords anywhere in query
    is_destructive, detected_keyword = contains_destructive_keywords(sql)
    
    if is_destructive:
        return False, f"Query contains forbidden keyword: {detected_keyword}"
    
    # Additional pattern checks for obfuscation attempts
    sql_upper = sql.upper()
    
    # Check for SQL injection patterns
    dangerous_patterns = [
        r';\s*DROP',
        r';\s*DELETE',
        r';\s*TRUNCATE',
        r';\s*ALTER',
        r';\s*UPDATE',
        r';\s*INSERT',
        r';\s*CREATE',
        r'UNION.*?(DELETE|DROP|UPDATE|INSERT|ALTER)',
        r'INTO\s+OUTFILE',
        r'INTO\s+DUMPFILE',
        r'LOAD_FILE',
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, sql_upper):
            return False, f"Query contains potentially malicious pattern: {pattern}"
    
    return True, ""


def validate_query(sql: str) -> Tuple[bool, str]:
    """
    Main validation function - convenience wrapper
    
    Args:
        sql: SQL query string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    return is_safe_query(sql)


def validate_multiple_queries(sql: str) -> Tuple[bool, str]:
    """
    Validate multiple SQL statements separated by semicolons
    
    Args:
        sql: String containing one or more SQL statements
        
    Returns:
        Tuple of (all_valid, error_message)
    """
    statements = [s.strip() for s in sql.split(';') if s.strip()]
    
    if not statements:
        return False, "No SQL statements found"
    
    for idx, stmt in enumerate(statements):
        is_valid, error_msg = is_safe_query(stmt)
        if not is_valid:
            return False, f"Statement {idx + 1}: {error_msg}"
    
    return True, ""
