from mysql.connector import Error
from utils.sql_validator import validate_query


def execute_query(connection, sql):
    # ✋ SECURITY CHECK: Validate query before execution
    is_valid, error_msg = validate_query(sql)
    if not is_valid:
        return f"🚫 BLOCKED: {error_msg}\n\nThis query is not allowed for security reasons.\nOnly read-only queries (SELECT, SHOW, DESCRIBE, EXPLAIN) are permitted."
    
    try:
        cursor = connection.cursor(buffered=True)
        cursor.execute(sql)

        # 🔑 This is the key line
        if cursor.with_rows:
            result = cursor.fetchall()
        else:
            connection.commit()
            result = "✔ Query executed successfully"

        cursor.close()
        return result

    except Error as e:
        try:
            cursor.close()
        except:
            pass
        return f"❌ SQL Error: {e}"
