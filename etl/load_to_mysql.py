import pandas as pd
import mysql.connector
import os
import json

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="helina123bikes",
    database="karamedical"
)
cursor = conn.cursor()

# Path to your JSON data folder
base_path = "data/raw/telegram_messages/2025-08-19"

inserted = 0
skipped = 0

# Traverse nested folders and files
for root, dirs, files in os.walk(base_path):
    for file in files:
        if not file.endswith(".json"):
            continue

        full_path = os.path.join(root, file)
        with open(full_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"⚠️ Failed to load JSON from {file}: {e}")
                skipped += 1
                continue

        # Convert JSON to DataFrame safely
        if isinstance(data, dict):
            df = pd.DataFrame([data])
        elif isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            print(f"⚠️ Unknown JSON structure in {file}")
            skipped += 1
            continue

        # Skip empty data
        if df.empty:
            continue

        # Extract channel info from filename
        channel_name = file.replace(".json", "")
        channel_url = f"https://t.me/{channel_name}"

        df["channel_name"] = channel_name
        df["channel_url"] = channel_url
        df["message_id"] = df["id"]
        df["message_date"] = pd.to_datetime(df["date"], errors="coerce")
        df["message_text"] = df.get("message", "")
        df["has_media"] = df.get("has_media", False)
        df["media_type"] = df.get("media_type", None)
        df["media_file_name"] = df.get("media_file_name", None)

        # Drop rows without message_id
        df = df.dropna(subset=["message_id"])

        print(f"🔹 Loading {len(df)} messages from channel: {channel_name}")

        for _, row in df.iterrows():
            try:
                cursor.execute("""
                    INSERT INTO raw_telegram_messages 
                    (message_id, message_date, message, channel_name, channel_url, has_media, media_type, media_file_name)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                        message=VALUES(message),
                        has_media=VALUES(has_media),
                        media_type=VALUES(media_type),
                        media_file_name=VALUES(media_file_name)
                """, (
                    int(row["message_id"]),
                    row["message_date"],
                    row["message_text"],
                    row["channel_name"],
                    row["channel_url"],
                    row["has_media"],
                    row["media_type"],
                    row["media_file_name"]
                ))
                inserted += 1
            except Exception as e:
                print(f"❌ Insert failed for message_id {row.get('message_id')}: {e}")
                skipped += 1

conn.commit()
cursor.close()
conn.close()

print(f"✅ Loaded {inserted} messages into raw_telegram_messages")
if skipped:
    print(f"⚠️ Skipped {skipped} rows due to errors")
