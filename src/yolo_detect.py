import os
import pandas as pd
from ultralytics import YOLO

model = YOLO('yolov8n.pt') 
IMAGE_FOLDER_PATH = "data/raw/images" 
results_list = []

print("Starting recursive scan...")


for root, dirs, files in os.walk(IMAGE_FOLDER_PATH):
    for filename in files:
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(root, filename)
            print(f"Processing: {img_path}")
            
            results = model(img_path)
            
            for result in results:
                detected_names = [model.names[int(c)] for c in result.boxes.cls]
                conf_scores = [float(c) for c in result.boxes.conf]
                
                has_person = 'person' in detected_names
                has_product = any(x in ['bottle', 'cup', 'vase', 'bowl'] for x in detected_names)

                if has_person and has_product:
                    category = "promotional"
                elif has_product and not has_person:
                    category = "product_display"
                elif has_person and not has_product:
                    category = "lifestyle"
                else:
                    category = "other"

                msg_id = os.path.splitext(filename)[0]

                results_list.append({
                    "message_id": msg_id,
                    "detected_objects": ", ".join(detected_names) if detected_names else "none",
                    "confidence_score": max(conf_scores) if conf_scores else 0,
                    "image_category": category
                })

# Save the final results
df = pd.DataFrame(results_list)
df.to_csv("yolo_results.csv", index=False)
print(f" Success! Found {len(results_list)} images and saved results to yolo_results.csv")