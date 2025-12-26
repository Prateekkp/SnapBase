from app.banner import show_banner
from config.store import load_config, save_config
from llm.generator import test_api_key, test_ollama_connection, generate_sql_with_ollama
from db.connection import connect_server, connect_database
from db.schema import list_databases, get_database_schema
from app.cli import start_cli
import sys
import os


def secure_input(prompt=""):
    """Get secure input with *** displayed as user types"""
    print(prompt, end="", flush=True)
    password = ""
    
    if os.name == 'nt':  # Windows
        import msvcrt
        while True:
            char = msvcrt.getwche()  # Read a character and echo it
            if char == '\r':  # Enter key
                print()  # New line after input
                break
            elif char == '\b':  # Backspace
                password = password[:-1]
                print('\b \b', end="", flush=True)  # Erase the last character
            else:
                password += char
                print('\b*', end="", flush=True)  # Replace with asterisk
    else:  # Unix/Linux/Mac
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            while True:
                char = sys.stdin.read(1)
                if char == '\n' or char == '\r':
                    print()
                    break
                elif char == '\x08' or char == '\x7f':  # Backspace
                    password = password[:-1]
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
                else:
                    password += char
                    sys.stdout.write('*')
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    return password


def main():
    show_banner()
    config = load_config()

    # Set default LLM provider if not set
    if "llm_provider" not in config:
        config["llm_provider"] = "nvidia"  # Default to NVIDIA

    # ---------- MAIN MENU ----------
    while True:
        print("\n" + "="*50)
        print("MAIN MENU")
        print("="*50)
        print("1. Start SnapBase (Query Database)")
        print("2. Manage API Key")
        print("3. Manage LLM Provider")
        print("4. Manage DB Profiles")
        print("5. Exit")
        
        main_choice = input("\nSelect option (1-5): ").strip()
        
        if main_choice == "1":
            if not config.get("api_key") and config.get("llm_provider") == "nvidia":
                print("❌ NVIDIA API key not configured. Please set it up first.")
                continue
            if config.get("llm_provider") == "ollama" and not test_ollama_connection():
                print("❌ Ollama not running. Please start Ollama first.")
                continue
            start_snapbase(config)
            
        elif main_choice == "2":
            manage_api_key(config)
            
        elif main_choice == "3":
            manage_llm_provider(config)
            
        elif main_choice == "4":
            manage_profiles(config)
            
        elif main_choice == "5":
            print("👋 Goodbye!")
            return
        else:
            print("⚠️ Invalid option, try again")


def manage_api_key(config):
    """Manage API Key operations"""
    while True:
        print("\n" + "="*50)
        print("API KEY MANAGEMENT")
        print("="*50)
        print("1. View API Key Status")
        print("2. Add/Update API Key")
        print("3. Delete API Key")
        print("4. Back to Main Menu")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            if config.get("api_key"):
                masked_key = config["api_key"][:10] + "***" + config["api_key"][-4:]
                print(f"✔ API Key: {masked_key}")
            else:
                print("❌ No API key saved")
                
        elif choice == "2":
            api_key = secure_input("Enter NVIDIA API key: ").strip()
            print("Validating API key...")
            if not test_api_key(api_key):
                print("❌ Invalid NVIDIA API key")
            else:
                config["api_key"] = api_key
                save_config(config)
                print("✔ API key validated and saved")
                
        elif choice == "3":
            if not config.get("api_key"):
                print("❌ No API key to delete")
            else:
                confirm = input("Are you sure you want to delete the API key? (yes/no): ").strip().lower()
                if confirm == "yes":
                    config["api_key"] = None
                    save_config(config)
                    print("✔ API key deleted")
                else:
                    print("❌ Deletion cancelled")
                    
        elif choice == "4":
            break
        else:
            print("⚠️ Invalid option, try again")


def manage_llm_provider(config):
    """Manage LLM Provider operations"""
    while True:
        print("\n" + "="*50)
        print("LLM PROVIDER MANAGEMENT")
        print("="*50)
        current_provider = config.get("llm_provider", "nvidia")
        print(f"Current LLM Provider: {current_provider.upper()}")
        print("\nAvailable providers:")
        print("1. NVIDIA (requires API key)")
        print("2. Ollama (runs locally)")
        print("3. Back to Main Menu")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            config["llm_provider"] = "nvidia"
            save_config(config)
            print("✔ LLM provider set to NVIDIA")
            
        elif choice == "2":
            if not test_ollama_connection():
                print("❌ Ollama is not running. Please start Ollama first.")
                print("Run 'ollama serve' in a terminal to start the Ollama service.")
            else:
                config["llm_provider"] = "ollama"
                save_config(config)
                print("✔ LLM provider set to Ollama")
                
        elif choice == "3":
            break
        else:
            print("⚠️ Invalid option, try again")


def manage_profiles(config):
    """Manage Database Profiles"""
    while True:
        print("\n" + "="*50)
        print("DATABASE PROFILE MANAGEMENT")
        print("="*50)
        
        if config["db_profiles"]:
            for i, p in enumerate(config["db_profiles"], 1):
                print(f"{i}. {p['user']}@{p['host']}")
        
        print(f"{len(config['db_profiles']) + 1}. Add new profile")
        print(f"{len(config['db_profiles']) + 2}. Back to Main Menu")
        
        choice = input("\nSelect option: ").strip()
        
        if choice.isdigit():
            choice_num = int(choice)
            profile_count = len(config["db_profiles"])
            
            if choice_num <= profile_count:
                profile_menu(config, choice_num - 1)
                
            elif choice_num == profile_count + 1:
                add_new_profile(config)
                
            elif choice_num == profile_count + 2:
                break
            else:
                print("⚠️ Invalid option")
        else:
            print("⚠️ Invalid option")


def profile_menu(config, profile_idx):
    """Menu for individual profile operations"""
    profile = config["db_profiles"][profile_idx]
    
    while True:
        print(f"\n{profile['user']}@{profile['host']}")
        print("-" * 50)
        print("1. Use this profile")
        print("2. Delete this profile")
        print("3. Back")
        
        choice = input("Select option (1-3): ").strip()
        
        if choice == "1":
            use_profile(config, profile_idx)
            return
            
        elif choice == "2":
            confirm = input(f"Delete profile {profile['user']}@{profile['host']}? (yes/no): ").strip().lower()
            if confirm == "yes":
                config["db_profiles"].pop(profile_idx)
                save_config(config)
                print("✔ Profile deleted")
                return
            else:
                print("❌ Deletion cancelled")
                
        elif choice == "3":
            return
        else:
            print("⚠️ Invalid option")


def use_profile(config, profile_idx):
    """Connect using a saved profile"""
    profile = config["db_profiles"][profile_idx]
    
    # Ask for password with secure input
    password = secure_input(f"Enter password for {profile['user']}: ").strip()
    
    try:
        server = connect_server(profile["host"], profile["user"], password)
    except Exception as e:
        print(f"❌ Cannot connect: {e}")
        return
    
    databases = list_databases(server)
    if not databases:
        print("❌ No databases found")
        server.close()
        return
    
    print("\nAvailable Databases:")
    for i, db in enumerate(databases, 1):
        print(f"{i}. {db}")
    
    while True:
        choice = input("Choose database number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(databases):
            db_name = databases[int(choice) - 1]
            break
        print("⚠️ Invalid selection, try again")
    
    server.close()
    
    # Connect to database
    conn = connect_database(profile["host"], profile["user"], password, db_name)
    print(f"✔ Connected to database: {db_name}")
    
    try:
        schema = get_database_schema(conn)
    except Exception as e:
        print(f"❌ Error loading schema: {e}")
        conn.close()
        return
    
    # Start CLI with database switching capability
    while True:
        action = start_cli(conn, schema, config.get("api_key"), config.get("llm_provider", "nvidia"))
        if action != "SWITCH_DB":
            break
        
        # Switch to different database
        try:
            conn.close()
            server = connect_server(profile["host"], profile["user"], password)
            databases = list_databases(server)
        except Exception as e:
            print(f"❌ Error connecting to server: {e}")
            return
        
        if not databases:
            print("❌ No databases found")
            server.close()
            return
        
        print("\nAvailable Databases:")
        for i, db in enumerate(databases, 1):
            print(f"{i}. {db}")
        
        while True:
            choice = input("Choose database number: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(databases):
                db_name = databases[int(choice) - 1]
                break
            print("⚠️ Invalid selection, try again")
        
        server.close()
        
        try:
            conn = connect_database(profile["host"], profile["user"], password, db_name)
            print(f"✔ Connected to database: {db_name}")
            schema = get_database_schema(conn)
        except Exception as e:
            print(f"❌ Error connecting to database: {e}")
            return
    
    conn.close()
    print("SnapBase session closed")


def add_new_profile(config):
    """Add a new database profile"""
    print("\n" + "="*50)
    print("ADD NEW DATABASE PROFILE")
    print("="*50)
    print("(Think of this like saving a bookmark to your favorite database)")
    
    # Validate inputs
    while True:
        host = input("DB Host (e.g., localhost, 192.168.1.1): ").strip()
        if not host:
            print("⚠️ Host cannot be empty")
            continue
        break
    
    while True:
        user = input("DB User: ").strip()
        if not user:
            print("⚠️ User cannot be empty")
            continue
        break
    
    password = secure_input("DB Password: ").strip()
    if not password:
        print("⚠️ Password cannot be empty")
        return
    
    # Test connection
    print("Testing connection...")
    try:
        server = connect_server(host, user, password)
        server.close()
        print("✔ Connection successful")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return
    
    config["db_profiles"].append({
        "host": host,
        "user": user,
        "password": password
    })
    save_config(config)
    print("✔ Profile saved successfully!")


def start_snapbase(config):
    """Start SnapBase with initial setup"""
    print("\n" + "="*50)
    print("START SNAPBASE")
    print("="*50)
    print("(Think of profiles like saving your favorite database bookmarks)")
    
    if not config["db_profiles"]:
        print("\nNo saved profiles. Let's create one!")
        add_new_profile(config)
        if not config["db_profiles"]:
            return
    
    # Show profiles
    print("\nSaved DB Profiles:")
    for i, p in enumerate(config["db_profiles"], 1):
        print(f"{i}. {p['user']}@{p['host']}")
    print(f"{len(config['db_profiles']) + 1}. Add new profile")
    
    choice = input("Select profile: ").strip()
    
    if choice.isdigit():
        choice_num = int(choice)
        profile_count = len(config["db_profiles"])
        
        if choice_num <= profile_count:
            use_profile(config, choice_num - 1)
        elif choice_num == profile_count + 1:
            add_new_profile(config)
        else:
            print("⚠️ Invalid option")


if __name__ == "__main__":
    main()
