import os

from ultralytics import YOLO
import cv2

def detect_number_plate_method_newOne_rename_later(frame):
    pass

def detect_number_plate_method():

    VIDEOS_DIR = os.path.join('.', 'Python', 'videos')

    video_path = os.path.join(VIDEOS_DIR, 'cars2.mp4')

    cap = cv2.VideoCapture(video_path)

    ret, frame = cap.read()


    H, W, _ = frame.shape

    count = 0
    frame_counter = 1
    frame_read = 20 #read every 20th frame


    #out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'mp4v'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

    model_path = os.path.join('.', 'Python', 'runs', 'detect', 'train', 'weights', 'last.pt')

    # Load a model
    model = YOLO(model_path)  # load a custom model

    threshold = 0.5

    while ret:

        if frame_counter % frame_read == 0:
            frame_counter += 1

            frame = cv2.resize(frame, (1920, 1080))

            results = model(frame)[0]

            for result in results.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = result

                print(x1, y1, x2, y2, score)

                if score > threshold:
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                    cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
            
                    img_roi = frame[int(y1): int(y2), int(x1): int(x2)]
                    cv2.imshow("Roi", img_roi)

                    cv2.imwrite("Python/plates/scanned_img_" + str(count) + ".jpg", img_roi)
                    count += 1
        
        
            cv2.imshow("video", frame)
            cv2.waitKey(1)
        else:
            frame_counter += 1

        #out.write(frame)
        ret, frame = cap.read()

    cap.release()
    #out.release()
    cv2.destroyAllWindows()
