import json
import requests


with open("config.json") as f:
    config = json.load(f)

TOKEN = config['token']


send_message_url = "https://discord.com/api/v9/channels/{channel_id}/messages"
send_reaction_url = "https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me?location=Message%20Hover%20Bar&type=0"


def get_dm_channels():
    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json"
    }
    

    response = requests.get("https://discord.com/api/v9/users/@me/channels", headers=headers)
    
    if response.status_code == 200:
        return response.json()  
    else:
        print(f"Failed to retrieve DM channels: {response.status_code} - {response.text}")
        return []

def find_existing_dm_channel(user_id):
    dm_channels = get_dm_channels()
    

    for channel in dm_channels:
        if channel['type'] == 1 and channel['recipients'][0]['id'] == user_id:
            return channel['id']
    
    return None


def create_dm_channel(user_id):
    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json"
    }
    
    data = {
        "recipient_id": user_id
    }
    

    response = requests.post("https://discord.com/api/v9/users/@me/channels", headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['id']  
    else:
        print(f"Failed to create DM channel: {response.status_code} - {response.text}")
        return None


def send_dm(channel_id, message):
    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json"
    }
    
    data = {
        "content": message
    }
    
    response = requests.post(send_message_url.format(channel_id=channel_id), headers=headers, json=data)
    
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.status_code} - {response.text}")


def send_reaction(channel_id, message_id, reaction):
    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json"
    }

    response = requests.put(send_reaction_url.format(channel_id=channel_id, message_id=message_id, reaction=reaction), headers=headers)
    
    if response.status_code == 204:
        print("Reaction added successfully!")
    else:
        print(f"Failed to add reaction: {response.status_code} - {response.text}")


if __name__ == "__main__":
    user_id = input("Enter the Discord ID of the user: ")
    

    dm_channel = find_existing_dm_channel(user_id)
    
    if dm_channel:
        print(f"DM channel already exists: {dm_channel}")
    else:

        print("No existing DM channel, creating one...")
        dm_channel = create_dm_channel(user_id)
    
    option = input("Enter 1 to send a message, or 2 to add a reaction: ")

    if dm_channel and option == "1":
        message = input("Enter the message to send: ")
        send_dm(dm_channel, message)

    if dm_channel and option == "2":
        message_id = input("Enter the message ID: ")
        reaction = input("Enter the reaction to add: ")
        send_reaction(dm_channel, message_id, reaction)
