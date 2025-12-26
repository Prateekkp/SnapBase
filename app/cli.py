from utils.separators import sep
from utils.intent import is_direct_sql
from llm.propmt import build_prompt
from llm.generator import generate_sql
from db.executor import execute_query
from utils.sql_cleaner import extract_sql
from utils.formatter import print_table
from utils.sql_validator import validate_multiple_queries



def start_cli(conn, schema, api_key):
    while True:
        sep()
        user_input = input("SnapBase> ").strip()
        sep()

        if user_input.lower() == "exit":
            return "EXIT"

        if user_input == ":switch_db":
            return "SWITCH_DB"

        # ---------- CASE 1: Direct SQL ----------
        if is_direct_sql(user_input):
            sql = user_input
            print("Detected direct SQL input")

        # ---------- CASE 2: Natural Language ----------
        else:
            print("Detected natural language input")
            raw_output = generate_sql(build_prompt(user_input, schema), api_key)

            sql = extract_sql(raw_output)
            if not sql:
                if raw_output is None:
                    print("\n💡 TIP: You can use direct SQL commands instead:")
                    print("   • SHOW TABLES;")
                    print("   • SHOW DATABASES;")
                    print("   • DESCRIBE table_name;")
                    print("   • SELECT * FROM table_name LIMIT 10;")
                else:
                    print("❌ Could not extract valid SQL from LLM output.")
                    print("LLM response was:")
                    print(raw_output)
                continue

        print("\nGenerated SQL:")
        print(sql)
        sep()

        # ✋ SECURITY CHECK: Validate all SQL statements before execution
        is_valid, error_msg = validate_multiple_queries(sql)
        if not is_valid:
            print(f"🚫 SECURITY BLOCK: {error_msg}")
            print("\n⚠️  Only read-only queries (SELECT, SHOW, DESCRIBE, EXPLAIN) are allowed.")
            print("    Destructive operations (DROP, DELETE, UPDATE, INSERT, etc.) are blocked.")
            continue

        # Split multiple SQL statements and execute each
        sql_statements = [s.strip() for s in sql.split(";") if s.strip()]
        
        for single_sql in sql_statements:
            result = execute_query(conn, single_sql)
            if isinstance(result, list) and result:
                # Get headers from cursor
                try:
                    cursor = conn.cursor(buffered=True)
                    cursor.execute(single_sql)
                    headers = [desc[0] for desc in cursor.description]
                    cursor.close()
                    
                    # Check if result has more than 20 rows
                    total_rows = len(result)
                    if total_rows > 20:
                        print_table(headers, result[:20])
                        print(f"\n⚠️ Showing 20 of {total_rows} rows. Use LIMIT clause to fetch more rows.")
                    else:
                        print_table(headers, result)
                except Exception as e:
                    print(f"❌ Error formatting result: {e}")
                    print(result)
            else:
                print(result)
