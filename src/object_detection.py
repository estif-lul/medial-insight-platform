from ultralytics import YOLO
import os, logging
from sqlalchemy import create_engine, text, exc
import cv2
from dotenv import load_dotenv
import random

load_dotenv('.env', override=True)
DB_URL = os.getenv('POSTGRES_URL')



class ObjectDetector:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.model = YOLO('models/yolov8l.pt')
        # Setup logging
        logging.basicConfig(filename='logs/detection.log', level=logging.INFO)

    def detect_object(self, image_path, message_id, channel_name):
        try:
            results = self.model(image_path)
            detections = []
            for box in results[0].boxes.data.tolist():
                x1, y1, x2, y2, conf, class_id = box
                if conf < 0.5: # Filter low-confidence
                    continue
                label = results[0].names[int(class_id)]
                detections.append({
                    'message_id': message_id,
                    'channel_name': channel_name,
                    'class': label,
                    'confidence': round(conf, 3),
                    'bbox': [round(x1), round(y1), round(x2), round(y2)]
                })
            return detections
        except Exception as e:
            logging.error(f'Detection failed for {image_path}: {e}')
            return []
    
    def process_images(self, image_dir):
        image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
        max = len(image_files)
        print(type(max))
        random_nums = self.generate_rand_num_list(1000)
        print (random_nums)
        for i, file in enumerate(image_files):
            path = os.path.join(image_dir, file)
            
            message_id = file.split('.')[0].replace('@', '')
            channel_name = file.split('_')[0].replace('@', '')
            
            detections = self.detect_object(path, message_id, channel_name)
            # all_detections.append(detections)

            try:
                with self.engine.begin() as conn:
                    for det in detections:
                        conn.execute(text("""
                            INSERT INTO fct_image_detections (message_id, detected_object_class, confidence_score, channel_name)
                            VALUES (:message_id, :class, :confidence, :channel_name)
                        """), det)
                logging.info(f"Processed {file} with {len(detections)} detections")
                if i in random_nums:
                    self.visualize(path, detections)
            except exc.IntegrityError as e:
                logging.error(f'Error occures during image detection: {e}')
                continue

            

    def visualize(self, image_path, detections):
        img = cv2.imread(image_path)
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, f'{det['class']} {det['confidence']}', (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.imwrite(f'data/processed/photos/{image_path.split('/')[-1]}', img)

    def generate_rand_num_list(self, max, n: int = 50):
        random_numbers = [random.randint(0, max) for _ in range(n)]
        logging.info(f'Generated random numbers: {random_numbers}')
        return random_numbers

if __name__ == '__main__':
    image_dir = 'data/raw/photos'
    detector = ObjectDetector(DB_URL)
    detector.process_images(image_dir)