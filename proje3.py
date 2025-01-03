import cv2
import numpy as np
import time

OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.legacy.TrackerCSRT_create,
    "kcf": cv2.legacy.TrackerKCF_create,
    "boosting": cv2.legacy.TrackerBoosting_create,
    "mil": cv2.legacy.TrackerMIL_create,
    "tld": cv2.legacy.TrackerTLD_create,
    "medianflow": cv2.legacy.TrackerMedianFlow_create,
    "mosse": cv2.legacy.TrackerMOSSE_create
}


tracker_name = "csrt"
trackers = cv2.legacy.MultiTracker_create()

video_path = "video.mp4"
cap = cv2.VideoCapture(video_path)



frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


start_time = time.time()


while True:
    if not paused:
            ret, frame = cap.read()

            frame = cv2.resize(frame, dsize=(960, 540))


            success, boxes = trackers.update(frame)


            for i, box in enumerate(boxes):
                (x, y, w, h) = [int(v) for v in box]
                cv2.rectangle(frame, (x, y), (x + w, y + h), 2)
                cv2.putText(frame, f"insan {i+1}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)

            cv2.imshow("Frame", frame)


    key = cv2.waitKey(10) & 0xFF
    if key == ord('s'):
        box = cv2.selectROI("Frame", frame, fromCenter=False)
        if box != (0, 0, 0, 0):
            tracker = OPENCV_OBJECT_TRACKERS[tracker_name]()
            trackers.add(tracker, frame, box)
        else:
            print("Geçersiz ROI seçimi.")
    elif key == ord('r'):
        trackers = cv2.legacy.MultiTracker_create()
    elif key == ord('p'):
        paused = not paused
        state = "Devam ediyor" if not paused else "Duraklatıldı"
        print(state)
  
  
    elif key == ord('q'):
        break




cap.release()
cv2.destroyAllWindows()