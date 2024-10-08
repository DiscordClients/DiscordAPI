import json
import requests


with open("config.json") as f:
    config = json.load(f)

TOKEN = config['token']


send_message_url = "https://discord.com/api/v9/channels/{channel_id}/messages"


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


if __name__ == "__main__":
    user_id = input("Enter the Discord ID of the user: ")
    

    dm_channel = find_existing_dm_channel(user_id)
    
    if dm_channel:
        print(f"DM channel already exists: {dm_channel}")
    else:

        print("No existing DM channel, creating one...")
        dm_channel = create_dm_channel(user_id)
    
    if dm_channel:
        message = input("Enter the message to send: ")
        send_dm(dm_channel, message)
