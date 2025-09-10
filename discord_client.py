import requests
from typing import Optional, List, Dict

class DiscordClient:
    BASE_URL = "https://discord.com/api/v9"

    def __init__(self, token: str):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": token,
            "Content-Type": "application/json"
        })

    def get_dm_channels(self) -> List[Dict]:
        url = f"{self.BASE_URL}/users/@me/channels"
        response = self.session.get(url)
        if response.ok:
            return response.json()
        raise Exception(f"Failed to retrieve DM channels: {response.status_code} - {response.text}")

    def find_existing_dm_channel(self, user_id: str) -> Optional[str]:
        for channel in self.get_dm_channels():
            if channel.get("type") == 1 and channel.get("recipients", [{}])[0].get("id") == user_id:
                return channel["id"]
        return None

    def create_dm_channel(self, user_id: str) -> str:
        url = f"{self.BASE_URL}/users/@me/channels"
        payload = {"recipient_id": user_id}
        response = self.session.post(url, json=payload)
        if response.ok:
            return response.json()["id"]
        raise Exception(f"Failed to create DM channel: {response.status_code} - {response.text}")

    def send_dm(self, channel_id: str, message: str) -> None:
        url = f"{self.BASE_URL}/channels/{channel_id}/messages"
        payload = {"content": message}
        response = self.session.post(url, json=payload)
        if response.ok:
            print("Message sent successfully!")
        else:
            raise Exception(f"Failed to send message: {response.status_code} - {response.text}")

    def send_reaction(self, channel_id: str, message_id: str, reaction: str) -> None:
        url = f"{self.BASE_URL}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me"
        response = self.session.put(url)
        if response.status_code == 204:
            print("Reaction added successfully!")
        else:
            raise Exception(f"Failed to add reaction: {response.status_code} - {response.text}")

    def get_all_messages(self, channel_id: str, limit: int = 100) -> List[Dict]:
        url = f"{self.BASE_URL}/channels/{channel_id}/messages"
        params = {"limit": limit}
        all_messages = []
        last_id = None

        while True:
            if last_id:
                params["before"] = last_id
            response = self.session.get(url, params=params)
            if not response.ok:
                raise Exception(f"Failed to fetch messages: {response.status_code} - {response.text}")

            messages = response.json()
            if not messages:
                break

            all_messages.extend(messages)
            last_id = messages[-1]["id"]
            if len(messages) < limit:
                break

        return all_messages
