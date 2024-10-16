import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import cv2
import sys

# Load the pre-trained MobileNet SSD model
def load_model():
    try:
        model_path="../object_detection_model/ssd-mobilenet-v2-tensorflow2-ssd-mobilenet-v2-v1"
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

def detect_objects(image, model):
    # Convert the float32 tensor to uint8
    input_tensor = tf.cast(image * 255, tf.uint8)
    detections = model(input_tensor)

    # Extract detection information
    boxes = detections['detection_boxes'].numpy()[0]
    classes = detections['detection_classes'].numpy()[0].astype(np.int32)
    scores = detections['detection_scores'].numpy()[0]
    return boxes, classes, scores

def visualize_results_limited(image, boxes, classes, scores, threshold=0.5):
    # Labels for limited set of objects
    labels = {1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 
              6: 'bus', 7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light'}
    
    return _visualize_results_helper(image, boxes, classes, scores, labels, threshold)

def visualize_results_extended(image, boxes, classes, scores, threshold=0.5):
    # Labels for COCO dataset (91 classes)
    labels = {1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus', 7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant', 13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat', 18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear', 24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag', 32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis', 36: 'snowboard', 37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove', 41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle', 46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon', 51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange', 56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut', 61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed', 67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse', 75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven', 80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock', 86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'}
    
    return _visualize_results_helper(image, boxes, classes, scores, labels, threshold)

def _visualize_results_helper(image, boxes, classes, scores, labels, threshold=0.5):
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
            label = f"{labels.get(class_id, 'Unknown')}: {int(score * 100)}%"
            cv2.putText(image, label, (start_point[0], start_point[1] - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return image

def main():
    # Load the model
    model = load_model()

    # Open the camera
    cap = cv2.VideoCapture(0)  # 0 for default camera

    if not cap.isOpened():
        print("Error: Could not open camera.")
        sys.exit(1)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break

        # Preprocess the image
        preprocessed_image = preprocess_image(frame)

        # Perform object detection
        boxes, classes, scores = detect_objects(preprocessed_image, model)

        # Visualize results
        confidence_threshold = 0.5  # You can adjust this value
        # Use either visualize_results_limited or visualize_results_extended
        # result_frame = visualize_results_limited(frame, boxes, classes, scores, threshold=confidence_threshold)
        # Alternatively, use the extended version:
        result_frame = visualize_results_extended(frame, boxes, classes, scores, threshold=confidence_threshold)

        # Display the resulting frame
        cv2.imshow('Real-time Object Detection', result_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
