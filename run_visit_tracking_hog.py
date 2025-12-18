import cv2
from visit_tracking import CentroidTracker

tracker = CentroidTracker()

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cap = cv2.VideoCapture("/home/she/Desktop/Watershopsystem/data/videos/cctv.mp4")

with open("visit_log.csv", "w") as f:
    f.write("track_id,entry_time,exit_time,duration_seconds\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rects, _ = hog.detectMultiScale(frame, winStride=(8,8))
    person_detections = []
    for (x, y, w, h) in rects:
        person_detections.append((x, y, x+w, y+h))

    tracker.update(person_detections)

cap.release()