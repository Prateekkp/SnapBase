from mysql.connector import Error


def execute_query(connection, sql):
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
