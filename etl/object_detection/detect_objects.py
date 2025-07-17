from pathlib import Path
import mysql.connector
from ultralytics import YOLO

def main():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="helina123bikes",
        database="kara_warehouse"
    )
    cursor = conn.cursor()

    model = YOLO('yolov8n.pt')

    image_root = Path("data/raw/images/")

    for image_path in image_root.rglob("*"):
        if image_path.suffix.lower() in [".png", ".jpg", ".jpeg"]:
            try:
                message_id = int(image_path.stem)  # filename without extension
            except ValueError:
                print(f"⚠️ Skipping file with invalid message_id: {image_path}")
                continue

            print(f"🖼️ Processing: {image_path}")
            results = model(str(image_path))

            for result in results:
                for box in result.boxes:
                    class_id = int(box.cls.cpu().numpy())
                    confidence = float(box.conf.cpu().numpy())
                    class_name = model.names[class_id]

                    print(f"📸 Detected '{class_name}' in message_id {message_id} with confidence {confidence:.2f}")

                    try:
                        cursor.execute("""
                            INSERT INTO fct_image_detections (media_file_name, detected_object_class, confidence_score)
                            VALUES (%s, %s, %s)
                            ON DUPLICATE KEY UPDATE confidence_score = VALUES(confidence_score)
                        """, (message_id, class_name, confidence))
                    except Exception as e:
                        print(f"❌ unable to detect object {message_id}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Finished loading detections")

if __name__ == "__main__":
    main()
