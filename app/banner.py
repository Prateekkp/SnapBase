def show_banner():
    # ANSI Color Codes
    BLUE = '\033[38;5;33m'    # Deep sky blue
    BOLD = '\033[1m'
    END = '\033[0m'

    # Using rf"" (raw f-string) to handle backslashes correctly
    # Added precise alignment for the border bars
    banner = rf"""{BLUE}{BOLD}
==========================================================
   _____                               ____                 
  / ___/ ____   ____ _ ____           / __ ) ____ _ _____ ___ 
  \__ \ / __ \ / __ `// __ \         / __  |/ __ `// ___// _ \
 ___/ // / / // /_/ // /_/ /        / /_/ // /_/ /(__  )/  __/
/____//_/ /_/ \__,_// .___/        /_____/ \__,_//____/ \___/ 
                   /_/                                        
=========================================================={END}
"""
    
    print(banner)

if __name__ == "__main__":
    show_banner()