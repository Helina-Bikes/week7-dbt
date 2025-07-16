import pandas as pd
import mysql.connector
import os
import json

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="helina123bikes",
    database="kara_warehouse"
)
cursor = conn.cursor()

# Path to your JSON data folder
base_path = "data/raw/telegram_messages/"

inserted = 0
skipped = 0

# Traverse nested folders and files
for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith(".json"):
            full_path = os.path.join(root, file)
            with open(full_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except Exception as e:
                    print(f"⚠️ Failed to load JSON from {file}: {e}")
                    continue

            # Handle both single dict and list
            df = pd.DataFrame([data] if isinstance(data, dict) else data)

            # Skip empty data
            if df.empty:
                continue

            # Extract channel info from filename
            file_name = os.path.basename(file)
            channel_name = file_name.replace(".json", "")
            channel_url = f"https://t.me/{channel_name}"

            df["channel_name"] = channel_name
            df["channel_url"] = channel_url
            df["message_id"] = df["id"]
            df["message_date"] = pd.to_datetime(df["date"], errors="coerce")

            # Drop rows without message_id
            df = df.dropna(subset=["message_id"])

            for _, row in df.iterrows():
                try:
                    cursor.execute("""
                        INSERT INTO raw_telegram_messages 
                        (message_id, message_date, message, channel_name, channel_url)
                        VALUES (%s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE message=VALUES(message)
                    """, (
                        int(row["message_id"]),
                        row["message_date"],
                        row.get("message", ""),
                        row["channel_name"],
                        row["channel_url"]
                    ))
                    inserted += 1
                except Exception as e:
                    print(f"❌ Insert failed for message_id {row.get('message_id')}: {e}")
                    skipped += 1

conn.commit()
cursor.close()
conn.close()

print(f"✅ Loaded {inserted} messages into raw_telegram_messages ✅")
if skipped:
    print(f"⚠️ Skipped {skipped} rows due to errors.")
