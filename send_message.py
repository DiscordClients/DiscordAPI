from discord_client import DiscordClient

def send_message(client: DiscordClient, user_id: str):
    dm_channel = client.find_existing_dm_channel(user_id) or client.create_dm_channel(user_id)
    message = input("Enter the message to send: ")
    client.send_dm(dm_channel, message)
