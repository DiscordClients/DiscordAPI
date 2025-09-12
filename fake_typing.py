from discord_client import DiscordClient
import time

def fake_typing(client: DiscordClient, user_id: str):
    dm_channel = client.find_existing_dm_channel(user_id)
    if not dm_channel:
        dm_channel = client.create_dm_channel(user_id)

    print(f"Simulating typing to user {user_id}. Press Ctrl+C to stop.")

    try:
        while True:
            url = f"https://discord.com/api/v9/channels/{dm_channel}/typing"
            response = client.session.post(url)
            if not response.ok:
                print(f"Failed to trigger typing: {response.status_code} - {response.text}")
                break
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nFake typing stopped. Returning to menu.")
        input("\nPress Enter to return to menu...")
