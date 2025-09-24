import os

from ultralytics import YOLO
import cv2

def detect_number_plate_method(frame):
    H, W, _ = frame.shape

    model_path = os.path.join('.', 'Python', 'runs', 'detect', 'train', 'weights', 'last.pt')

    # Load a model
    model = YOLO(model_path)  # load a custom model

    threshold = 0.5

    frame = cv2.resize(frame, (1920, 1080))

    results = model(frame)[0]

    img_counter = 0

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        print(x1, y1, x2, y2, score)

        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
            
            img_roi = frame[int(y1): int(y2), int(x1): int(x2)]

            cv2.imwrite(f"Python/plates/plate{img_counter}.jpg", img_roi)
            img_counter += 1

    cv2.destroyAllWindows()