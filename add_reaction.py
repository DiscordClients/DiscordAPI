from discord_client import DiscordClient

def add_reaction(client: DiscordClient, user_id: str):
    dm_channel = client.find_existing_dm_channel(user_id)
    if not dm_channel:
        dm_channel = client.create_dm_channel(user_id)


    message_id = input("Enter the message ID: ").strip()
    reaction = input("Enter the reaction to add (e.g., 🙂 or %F0%9F%99%82 for URL-encoded emoji): ").strip()

    try:
        client.send_reaction(dm_channel, message_id, reaction)  
        print(f"Reaction '{reaction}' added to message {message_id} in DM with user {user_id}.")
    except Exception as e:
        print(f"Failed to add reaction: {e}")

    input("\nPress Enter to return to menu...")
