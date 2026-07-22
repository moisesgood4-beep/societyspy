import os
import argparse
from datetime import datetime
from itertools import product

class TextColors:
    RED = "\033[91m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

ASCII_ART = """
\033[94m\033[1m      o  o   o  o\033[0m
\033[94m\033[1m      |\\/ \\^/ \\/|\033[0m         \033[93m█▀▄ ▄▀▄ ▄▀▀ ▄▀▀ █   ▄▀▄ █▀▄ █▀▄\033[0m
\033[94m\033[1m      |,-------.|\033[0m         \033[93m█▀  █▀█ ▄██ ▄██ █▄▄ ▀▄▀ █▀▄ █▄▀\033[0m
\033[94m\033[1m     ,-.\033[93m(|)   (|)\033[94m\033[1m,-.\033[0m                       \033[93mv2.0.1\033[0m
\033[94m\033[1m     \\_*._ ' '_.* _/\033[0m     \033[93m\033[1mAdvanced customizable wordlist generator
\033[94m\033[1m      /`-.`--' .-'\\\033[0m     ●━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━●\033[0m
\033[94m\033[1m ,--./    `---'    \\,--.\033[0m   ┃  https://github.com/navnee1h/passlord   ┃
\033[94m\033[1m \\   |( )     ( )|   /\033[0m   ●━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━●\033[0m
\033[94m\033[1m  \\  | ||       || |  /\033[0m   ✯ Edit rules.txt for personalized wordlist changes
\033[94m\033[1m   \\ | /|\\     /|\\ | /\033[0m    ✯ Input details about your target
\033[94m\033[1m   /  \\-._     _,-/  \\\033[0m    ✯ Skip the question by hitting Enter
\033[94m\033[1m  //| \\\\  `---'  // |\\\\\033[0m
\033[94m\033[1m /,-.,-.\\       /,-.,-.\\\033[0m
\033[94m\033[1m o   o   o       o   o   o\033[0m
"""

def apply_leet(word):
    """Applies common leet speak substitutions to a word."""
    substitutions = {'a': '@', 'e': '3', 'o': '0', 's': '$', 'l': '1', 'i': '!', 't': '7'}
    return ''.join(substitutions.get(char.lower(), char) for char in word)

def apply_toggle_case(word):
    """Applies tOGGLEcASE to a word."""
    return ''.join(c.lower() if i % 2 == 0 else c.upper() for i, c in enumerate(word))

def get_name_combinations(name_string, config):
    """Generates name variations based on configuration."""
    if not name_string:
        return []
    
    parts = [[word.lower(), word.title()] for word in name_string.split()]
    combinations = [''.join(combo) for combo in product(*parts)]
    
    if config.get('toggle_case', False):
        toggle_combinations = [apply_toggle_case(combo) for combo in combinations]
        combinations.extend(toggle_combinations)
        
    return list(dict.fromkeys(combinations))

def collect_user_info(config):
    """Collects all user inputs and returns them in a single dictionary."""
    info = {}
    print(f"{TextColors.BLUE}--- Enter Target Information (Press Enter to skip) ---{TextColors.RESET}")
    info['fname'] = get_name_combinations(input(f"{TextColors.BLUE}〘〙 First Name  : {TextColors.RESET}").strip(), config)
    info['mname'] = get_name_combinations(input(f"{TextColors.BLUE}〘〙 Middle Name : {TextColors.RESET}").strip(), config)
    info['lname'] = get_name_combinations(input(f"{TextColors.BLUE}〘〙 Last Name   : {TextColors.RESET}").strip(), config)
    info['nname'] = get_name_combinations(input(f"{TextColors.BLUE}〘〙 Nick Name   : {TextColors.RESET}").strip(), config)
    info['oname'] = get_name_combinations(input(f"{TextColors.BLUE}〘〙 Other Name  : {TextColors.RESET}").strip(), config)
    info['gf'] = get_name_combinations(input(f"{TextColors.BLUE}〘〙 Girl Friend : {TextColors.RESET}").strip(), config)
    info['house'] = get_name_combinations(input(f"{TextColors.BLUE}〘〙 House Name  : {TextColors.RESET}").strip(), config)
    info['pet'] = get_name_combinations(input(f"{TextColors.BLUE}〘〙 Pet Name    : {TextColors.RESET}").strip(), config)
    info['company'] = get_name_combinations(input(f"{TextColors.BLUE}〘〙 Company Name: {TextColors.RESET}").strip(), config)
    info['othername'] = get_name_combinations(input(f"{TextColors.BLUE}〘〙 Other keyword : {TextColors.RESET}").strip(), config)

    while True:
        dob_input = input(f"{TextColors.BLUE}〘〙 DoB (DD MM YYYY): {TextColors.RESET}").strip()
        if not dob_input:
            info['dob'], info['dyear'] = [], []
            break
        try:
            dob_date = datetime.strptime(dob_input, '%d %m %Y').date()
            info['dyear'] = [str(dob_date.year), dob_date.strftime("%y")]
            dob_formats = [
                dob_date.strftime("%d%m%Y"), dob_date.strftime("%d%m%y"),
                str(dob_date.day), dob_date.strftime("%d"),
                str(dob_date.month), dob_date.strftime("%m")
            ]
            if config.get('more_dates', False):
                dob_formats.extend([
                    dob_date.strftime("%Y%m%d"), dob_date.strftime("%d%B%Y"),
                    dob_date.strftime("%B")
                ])
            info['dob'] = list(dict.fromkeys(dob_formats))
            break
        except ValueError:
            print(f"{TextColors.RED}  ⭆ Invalid date format. Please use DD MM YYYY.{TextColors.RESET}")
    return info

def get_static_combinations(config):
    """Generates static keyword lists based on configuration."""
    static_info = {}
    year_range_str = config.get('year_range')
    if year_range_str:
        try:
            start, end = map(int, year_range_str.split('-'))
            static_info['years'] = [str(y) for y in range(start, end + 1)]
        except ValueError:
            print(f"{TextColors.RED}Invalid year range format. Using default.{TextColors.RESET}")
            static_info['years'] = [str(y) for y in range(1970, datetime.now().year + 1)]
    else:
        static_info['years'] = [str(y) for y in range(1970, datetime.now().year + 1)]

    static_info['symbols'] = list(config.get('symbols', '@_.'))
    static_info['rnum1'] = config.get('numbers1', ["123", "1234", "12345", "789"])
    static_info['rnum2'] = config.get('numbers2', ["11", "22", "33", "77", "88", "99", "777"])
    return static_info

def generate_wordlist(info, rules_path, config):
    """Generates a unique set of passwords based on rules and configuration."""
    unique_passwords = set()
    min_len = config.get('min_len', 6)
    max_len = config.get('max_len', 99)
    leet_on = config.get('leet', False)

    try:
        with open(rules_path, 'r') as rules_file:
            for line in rules_file:
                if not line.strip() or line.startswith('#'):
                    continue
                pointers = line.strip().split('@')
                component_lists = [info.get(p, []) for p in pointers]
                if any(not sublist for sublist in component_lists):
                    continue

                for combo in product(*component_lists):
                    password = ''.join(combo)
                    if min_len <= len(password) <= max_len:
                        unique_passwords.add(password)
                        if leet_on:
                            unique_passwords.add(apply_leet(password))
    except FileNotFoundError:
        print(f"{TextColors.RED}  ⭆ Error: The rules file was not found at '{rules_path}'.{TextColors.RESET}")
        return None
    except Exception as e:
        print(f"{TextColors.RED}  ⭆ An unexpected error occurred: {e}{TextColors.RESET}")
        return None
        
    return unique_passwords

def configure_advanced_mode():
    """Interactively asks the user for advanced settings."""
    config = {}
    print(f"\n{TextColors.YELLOW}--- Advanced Mode Configuration ---{TextColors.RESET}")
    print("Answer the following to customize your wordlist (press Enter for defaults).")

    try:
        config['min_len'] = int(input(f"{TextColors.BLUE}Enter minimum password length (default: 6): {TextColors.RESET}") or "6")
        config['max_len'] = int(input(f"{TextColors.BLUE}Enter maximum password length (default: 99): {TextColors.RESET}") or "99")
    except ValueError:
        print(f"{TextColors.RED}Invalid number. Using defaults.{TextColors.RESET}")
        config['min_len'], config['max_len'] = 6, 99
    
    config['leet'] = input(f"{TextColors.BLUE}Enable Leet Speak (e.g., a=@, e=3)? (y/n): {TextColors.RESET}").lower().strip() == 'y'
    config['more_dates'] = input(f"{TextColors.BLUE}Enable more date formats (e.g., 20251225)? (y/n): {TextColors.RESET}").lower().strip() == 'y'
    config['toggle_case'] = input(f"{TextColors.BLUE}Enable tOGGLEcASE variations? (y/n): {TextColors.RESET}").lower().strip() == 'y'

    if input(f"{TextColors.BLUE}Customize year range? (y/n): {TextColors.RESET}").lower().strip() == 'y':
        config['year_range'] = input(f"  Enter year range (e.g., 2000-2025): {TextColors.RESET}").strip()
    
    if input(f"{TextColors.BLUE}Customize symbols? (y/n): {TextColors.RESET}").lower().strip() == 'y':
        config['symbols'] = input(f"  Enter all symbols without spaces (e.g., @!#$): {TextColors.RESET}").strip()
        
    print(f"{TextColors.YELLOW}--- Configuration Set ---{TextColors.RESET}")
    return config

def main():
    """Main function with interactive advanced mode."""
    # Print the ASCII art first, regardless of mode.
    print(ASCII_ART)

    parser = argparse.ArgumentParser(description="Advanced customizable wordlist generator.")
    parser.add_argument('-A', '--advanced', action='store_true', help="Run in interactive Advanced Mode.")
    args = parser.parse_args()

    config = {}
    if args.advanced:
        config = configure_advanced_mode()
    else:
        print("\nRunning in Simple Mode. For more options, run with the -A or --advanced flag.")
        config = {
            'min_len': 6, 'max_len': 99, 'leet': False, 
            'more_dates': False, 'toggle_case': False
        }

    try:
        rules_path = os.path.join("patterns", "rules.txt")
        if not os.path.isfile(rules_path):
            print(f"{TextColors.RED}Error! 'rules.txt' not found. Make sure it's inside a 'patterns' sub-directory.{TextColors.RESET}")
            return
        
        all_info = {}
        all_info.update(collect_user_info(config))
        all_info.update(get_static_combinations(config))
        
        wordlist = generate_wordlist(all_info, rules_path, config)
        
        if wordlist is None: return
        if not wordlist:
            print(f"\n{TextColors.RED}No passwords could be generated.{TextColors.RESET}")
            return
            
        while True:
            output_file_name = input(f"\n{TextColors.BLUE}〘〙 Enter the output file name: {TextColors.RESET}").strip()
            if output_file_name:
                break
            print(f"{TextColors.RED}  ⭆ Output file name cannot be blank.{TextColors.RESET}")
        
        output_file_path = os.path.join(os.getcwd(), output_file_name)
        with open(output_file_path, 'w') as f:
            for password in sorted(list(wordlist)):
                f.write(f"{password}\n")
                
        print(f"\n{TextColors.BLUE}Success! {len(wordlist)} unique passwords have been generated.{TextColors.RESET}")
        print(f"{TextColors.BLUE}File saved at: {output_file_path}{TextColors.RESET}")

    except KeyboardInterrupt:
        print(f"\n\n{TextColors.RED}\033[1mExiting....\033[0m")
    except Exception as e:
        print(f"\n{TextColors.RED}A critical error occurred: {e}{TextColors.RESET}")

if __name__ == "__main__":
    main()
