import cv2

# Define class labels for the MobileNet SSD model
classes = ["background", "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", 
           "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", 
           "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", 
           "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat", 
           "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup", 
           "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", 
           "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table", 
           "toilet", "TV", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", 
           "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", 
           "hair drier", "toothbrush"]

# Load the pre-trained MobileNet SSD model
model = cv2.dnn.readNetFromTensorflow("ssd_mobilenet_v2_coco.pb", "ssd_mobilenet_v2_coco.pbtxt")

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture each frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
    model.setInput(blob)
    detections = model.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            class_id = int(detections[0, 0, i, 1])
            class_name = classes[class_id] if class_id < len(classes) else "Unknown"
            box = detections[0, 0, i, 3:7] * [w, h, w, h]
            (startX, startY, endX, endY) = box.astype("int")

            # Draw the rectangle and label on the frame
            label = f"{class_name}: {confidence * 100:.2f}%"
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("Webcam Object Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
