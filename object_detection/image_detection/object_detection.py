import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import cv2
import sys
import ssl
import os
import tempfile
import certifi

# Load the pre-trained MobileNet SSD model
def load_model():
    try:
        model_path="../object_detection_model/objecssd-mobilenet-v2-tensorflow2-ssd-mobilenet-v2-v1"
        model = hub.load(model_path)
        print("Model loaded successfully!")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)


def preprocess_image(image):
    # Resize and normalize the image
    img_resized = cv2.resize(image, (320, 320))
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    img_normalized = img_rgb / 255.0  # Normalize to [0,1]
    return np.expand_dims(img_normalized, axis=0)  # Add batch dimension


def detect_objects(image):
    # Convert the float32 tensor to uint8
    input_tensor = tf.cast(image * 255, tf.uint8)
    detections = model(input_tensor)

    # Extract detection information
    boxes = detections['detection_boxes'].numpy()[0]
    classes = detections['detection_classes'].numpy()[0].astype(np.int32)
    scores = detections['detection_scores'].numpy()[0]
    return boxes, classes, scores


def visualize_results(image, boxes, classes, scores, threshold=0.5):
    # Labels for COCO dataset
    labels = {1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 
              6: 'bus', 7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light'}
    
    # Loop over detections and draw them
    for i in range(len(scores)):
        if scores[i] >= threshold:
            box = boxes[i]
            class_id = classes[i]
            score = scores[i]
            
            # Scale box coordinates back to image size
            h, w, _ = image.shape
            start_point = (int(box[1] * w), int(box[0] * h))
            end_point = (int(box[3] * w), int(box[2] * h))
            
            # Draw the box
            cv2.rectangle(image, start_point, end_point, (0, 255, 0), 2)
            label = f"{labels[class_id]}: {int(score * 100)}%"
            cv2.putText(image, label, (start_point[0], start_point[1] - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Show the output image
    cv2.imshow("Object Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    # Load the model
    global model
    model = load_model()

    # Load the image
    image_path = "image1.jpg"  # Change this to the path of your image
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found or could not be read")
    except Exception as e:
        print(f"Error loading image: {e}")
        sys.exit(1)

    # Preprocess the image
    preprocessed_image = preprocess_image(image)

    # Perform object detection
    boxes, classes, scores = detect_objects(preprocessed_image)

    # Visualize results
    confidence_threshold = 0.5  # You can adjust this value
    visualize_results(image, boxes, classes, scores, threshold=confidence_threshold)

if __name__ == "__main__":
    main()
