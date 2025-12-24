def list_databases(conn):
    cur = conn.cursor()
    cur.execute("SHOW DATABASES")
    dbs = [x[0] for x in cur.fetchall()]
    cur.close()
    return dbs

def table_schema(conn, table):
    cur = conn.cursor()
    cur.execute(f"DESCRIBE {table}")
    schema = cur.fetchall()
    cur.close()
    return schema

def get_database_schema(conn):
    """Get all tables and their columns for the current database"""
    cur = conn.cursor()
    cur.execute("SHOW TABLES")
    tables = [x[0] for x in cur.fetchall()]
    
    schema = []
    for table in tables:
        cur.execute(f"DESCRIBE {table}")
        columns = cur.fetchall()
        for col in columns:
            col_name = col[0]
            col_type = col[1]
            schema.append((table, col_name, col_type))
    
    cur.close()
    return schema