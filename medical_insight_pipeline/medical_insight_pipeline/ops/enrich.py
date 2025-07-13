from dagster import op

import sys
sys.path.insert(1, '../src')
from object_detection import ObjectDetector

@op
def run_yolo_enrichement():
    image_dir = 'data/raw/photos'
    detector = ObjectDetector()
    detector.process_images(image_dir)
    return "YOLO enrichment complete"