import os
import json
import time
import random
import string
from pynput.keyboard import Controller
from colorama import Fore, Style, init

init(autoreset=True)

keyboard = Controller()
DATA_FILE = os.path.join(os.getcwd(), "data.json")

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def generate_random_key(length=12, use_upper=True, use_lower=True, use_digits=True, use_special=True):
    char_pool = ''
    if use_upper: char_pool += string.ascii_uppercase
    if use_lower: char_pool += string.ascii_lowercase
    if use_digits: char_pool += string.digits
    if use_special: char_pool += string.punctuation

    if not char_pool:
        raise ValueError("At least one character type must be selected")

    return ''.join(random.choice(char_pool) for _ in range(length))

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def pause_and_clear(msg=""):
    if msg:
        print(msg)
    time.sleep(1)
    clear()

while True:
    clear()
    data = load_data()
    keys = list(data.keys())

    print(Fore.CYAN + Style.BRIGHT + "\n=========== [[ NOTE MANAGER ]] ===========\n")
    print(Fore.YELLOW + "0. New Note")
    if keys:
        print(Fore.GREEN + "\n---------- Your Notes ----------")
        for idx, key in enumerate(keys, 1):
            title = data[key]['title']
            print(f"{idx}. {title}")
    else:
        print(Fore.RED + "\n(No notes available)")
    print(Fore.CYAN + "\n===========================================\n")

    try:
        choice = int(input("Select an option: "))
    except ValueError:
        pause_and_clear(Fore.RED + "Invalid input! Please enter a number.")
        continue

    if choice == 0:
        clear()
        print(Fore.MAGENTA + "Write your note and press Enter:\n")
        content = input("> ")
        key = generate_random_key()
        title = (content[:20] + "...") if len(content) > 20 else content
        data[key] = {
            "title": title,
            "length": len(content),
            "content": content
        }
        save_data(data)
        pause_and_clear(Fore.GREEN + "[[ NOTE SAVED ]]")

    elif 1 <= choice <= len(keys):
        key = keys[choice - 1]
        note = data[key]
        
        while True:
            clear()
            print()
            print(Fore.YELLOW + f"{note['title']}\n")
            print(Fore.WHITE + note['content'] + "\n")
            print(Fore.GREEN + f"{note['length']} characters\n\n")

            print("1. Edit Content")
            print("2. Rename Title")
            print("3. Delete Note")
            print("0. Back to Main Menu\n")

            try:
                sub_action = int(input("Choose an action: "))
            except ValueError:
                pause_and_clear(Fore.RED + "Please enter a valid number.")
                continue

            if sub_action == 0:
                break

            elif sub_action == 1:
                clear()
                print(Fore.MAGENTA + "Edit your note (leave blank to cancel):\n")
                keyboard.type(note['content'])
                updated = input()
                if updated.strip():
                    note['content'] = updated
                    note['length'] = len(updated)
                    data[key] = note
                    save_data(data)
                    pause_and_clear(Fore.GREEN + "[[ NOTE UPDATED ]]")
                else:
                    pause_and_clear(Fore.YELLOW + "[[ No changes made ]]")

            elif sub_action == 2:
                clear()
                print(Fore.MAGENTA + "Enter new title (leave blank to cancel):")
                new_title = input("> ").strip()
                if new_title:
                    note['title'] = new_title
                    data[key] = note
                    save_data(data)
                    pause_and_clear(Fore.GREEN + "[[ TITLE UPDATED ]]")
                else:
                    pause_and_clear(Fore.YELLOW + "[[ Title unchanged ]]")

            elif sub_action == 3:
                confirm = input(Fore.RED + "Are you sure you want to delete this note? (y/N): ")
                if confirm.lower() == 'y':
                    del data[key]
                    save_data(data)
                    pause_and_clear(Fore.RED + "[[ NOTE DELETED ]]")
                    break
                else:
                    pause_and_clear(Fore.YELLOW + "[[ Deletion cancelled ]]")

            else:
                pause_and_clear(Fore.RED + "Invalid option.")

    elif choice == 99:
        clear()
        confirm = input(Fore.RED + "Are you sure you want to delete ALL notes? (y/N): ")
        if confirm.lower() == 'y':
            save_data({})
            pause_and_clear(Fore.RED + "All notes deleted.")

    else:
        pause_and_clear(Fore.RED + "Invalid option selected.")
