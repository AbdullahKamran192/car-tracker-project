import os

from ultralytics import YOLO
import cv2


#VIDEOS_DIR = os.path.join('.', 'videos')

#video_path = os.path.join(VIDEOS_DIR, 'cars1.mp4')
#video_path_out = '{}_out.mp4'.format(video_path)

rtsp_link = "rtsp:admin:@192.168.1.41:554/stream1"

cap = cv2.VideoCapture(rtsp_link)

ret, frame = cap.read()


H, W, _ = frame.shape


#out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'mp4v'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

model_path = os.path.join('.', 'runs', 'detect', 'train', 'weights', 'last.pt')

# Load a model
model = YOLO(model_path)  # load a custom model

threshold = 0.5

while ret:

    frame = cv2.resize(frame, (1920, 1080))

    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
        
        
    cv2.imshow("video", frame)
    cv2.waitKey(1)

    #out.write(frame)
    ret, frame = cap.read()

cap.release()
#out.release()
cv2.destroyAllWindows()