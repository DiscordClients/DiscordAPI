import os
import time
from datetime import datetime
from discord_client import DiscordClient

def message_logger(client: DiscordClient, user_id: str):
    dm_channel = client.find_existing_dm_channel(user_id) or client.create_dm_channel(user_id)
    log_file = f"messages_{user_id}.log"
    print(f"Message Logger enabled. Logging to {log_file}. Press Ctrl+C to stop.\n")

    last_seen = {}
    lines = []
    written_dates = set()
    latest_id = None

    print("Fetching full DM history...")
    messages = client.get_all_messages(dm_channel, limit=100)
    messages.sort(key=lambda m: int(m["id"]))  

    for msg in messages:
        msg_id = msg["id"]
        author = msg["author"]["username"]
        content = msg.get("content", "")
        timestamp = msg.get("timestamp", "")
        date_str = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).strftime("%Y-%m-%d")
        header = f"=== {date_str} ==="

        if header not in written_dates:
            lines.append(header)
            written_dates.add(header)

        line_index = len(lines)
        lines.append(f"[{author}]: {content}")
        last_seen[msg_id] = {"content": content, "line_index": line_index}
        latest_id = msg_id


    with open(log_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Finished fetching {len(messages)} messages. Now monitoring for new changes...")

    try:
        while True:
            new_messages = client.get_all_messages(dm_channel, limit=100)
            new_messages = [m for m in new_messages if int(m["id"]) > int(latest_id)]
            new_messages.sort(key=lambda m: int(m["id"])) 

            current_ids = set(last_seen.keys())

            for msg in new_messages:
                msg_id = msg["id"]
                author = msg["author"]["username"]
                content = msg.get("content", "")
                timestamp = msg.get("timestamp", "")
                date_str = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).strftime("%Y-%m-%d")
                header = f"=== {date_str} ==="

                if header not in written_dates:
                    lines.append(header)
                    written_dates.add(header)
                    with open(log_file, "a", encoding="utf-8") as f:
                        f.write(f"\n{header}\n")

                line_index = len(lines)
                lines.append(f"[{author}]: {content}")
                last_seen[msg_id] = {"content": content, "line_index": line_index}
                latest_id = msg_id

                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"[{author}]: {content}\n")

            all_messages = client.get_all_messages(dm_channel, limit=100)
            for msg in all_messages:
                msg_id = msg["id"]
                if msg_id in last_seen:
                    old_content = last_seen[msg_id]["content"]
                    new_content = msg.get("content", "")
                    if old_content != new_content:
                        line_index = last_seen[msg_id]["line_index"]
                        lines[line_index] = f"{lines[line_index]} <EDITED> {new_content}"
                        last_seen[msg_id]["content"] = new_content

                        with open(log_file, "r+", encoding="utf-8") as f:
                            file_lines = f.read().splitlines()
                            file_lines[line_index] = lines[line_index]
                            f.seek(0)
                            f.write("\n".join(file_lines))
                            f.truncate()

            all_ids = {m["id"] for m in all_messages}
            deleted_ids = [mid for mid in last_seen if mid not in all_ids]
            for mid in deleted_ids:
                line_index = last_seen[mid]["line_index"]
                if "<DELETED>" not in lines[line_index]:
                    lines[line_index] = f"{lines[line_index]} <DELETED>"

                    with open(log_file, "r+", encoding="utf-8") as f:
                        file_lines = f.read().splitlines()
                        file_lines[line_index] = lines[line_index]
                        f.seek(0)
                        f.write("\n".join(file_lines))
                        f.truncate()

                del last_seen[mid]

            time.sleep(2)

    except KeyboardInterrupt:
        print("\nMessage Logger stopped. Returning to menu...")
