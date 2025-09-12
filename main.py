import json
import os
import platform
from discord_client import DiscordClient
from send_message import send_message
from add_reaction import add_reaction
from message_logger import message_logger
from fake_typing import fake_typing

def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")

def load_config():
    if os.path.exists("config.json"):
        with open("config.json") as f:
            return json.load(f)
    return {}

def save_config(config):
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

def get_valid_user_id():
    while True:
        uid = input("Enter the Discord ID of the user: ").strip()
        if uid.isdigit():
            return uid
        print("Invalid ID. Discord IDs are numeric.")

def main_menu(client, config):
    user_id = config.get("user_id")
    if not user_id:
        user_id = get_valid_user_id()
        config["user_id"] = user_id
        save_config(config)

    while True:
        clear_screen()
        print("Options:")
        print("1. Send a message")
        print("2. Add a reaction")
        print("3. Fake typing")
        print("4. Message Logger")
        print("5. Change Discord ID")
        print("6. Change Token")
        print("7. Exit")

        option = input("Choose an option: ").strip()

        try:
            if option == "1":
                send_message(client, user_id)
            elif option == "2":
                add_reaction(client, user_id)
            elif option == "3":
                fake_typing(client, user_id)
            elif option == "4":
                message_logger(client, user_id)
            elif option == "5":
                user_id = get_valid_user_id()
                config["user_id"] = user_id
                save_config(config)
                print("Discord ID updated!")
                input("\nPress Enter to return to menu...")
            elif option == "6":
                new_token = input("Enter new Discord token: ").strip()
                if new_token:
                    config["token"] = new_token
                    save_config(config)
                    print("Token updated successfully!")
                    input("\nPress Enter to return to menu...")
                    client = DiscordClient(new_token)
                else:
                    print("Invalid token.")
                    input("\nPress Enter to return to menu...")
            elif option == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid option.")
                input("\nPress Enter to return to menu...")

        except Exception as e:
            print(f"\nError: {e}")
            input("\nPress Enter to return to menu...")

if __name__ == "__main__":
    config = load_config()
    token = config.get("token")
    if not token:
        raise ValueError("Token not found in config.json!")
    client = DiscordClient(token)
    main_menu(client, config)
