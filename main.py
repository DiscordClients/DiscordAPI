import json
import os
import platform
from discord_client import DiscordClient
from send_message import send_message
from add_reaction import add_reaction
from message_logger import message_logger

def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")

def load_config():
    if os.path.exists("config.json"):
        with open("config.json") as f:
            return json.load(f)
    return {}

def save_config(config):
    with open("config.json", "w") as f:
        import json
        json.dump(config, f, indent=4)

if __name__ == "__main__":
    config = load_config()
    token = config.get("token")
    if not token:
        raise ValueError("Token not found in config.json!")

    client = DiscordClient(token)

    user_id = config.get("user_id")
    if not user_id:
        user_id = input("Enter the Discord ID of the user: ")
        config["user_id"] = user_id
        save_config(config)

    while True:
        clear_screen()
        print("Options:")
        print("1. Send a message")
        print("2. Add a reaction")
        print("3. Change Discord ID")
        print("4. Message Logger")
        print("5. Exit")

        option = input("Choose an option: ").strip()

        try:
            if option == "1":
                send_message(client, user_id)

            elif option == "2":
                add_reaction(client, user_id)

            elif option == "3":
                user_id = input("Enter new Discord ID: ")
                config["user_id"] = user_id
                save_config(config)
                print("Discord ID updated!")
                input("\nPress Enter to return to menu...")

            elif option == "4":
                message_logger(client, user_id)

            elif option == "5":
                print("Goodbye!")
                break

            else:
                print("Invalid option.")
                input("\nPress Enter to return to menu...")

        except Exception as e:
            print(f"\nError: {e}")
            input("\nPress Enter to return to menu...")
