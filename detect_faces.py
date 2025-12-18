import os
import cv2
import numpy as np
from insightface.app import FaceAnalysis


FRAMES_DIR =  "/home/she/Desktop/Watershopsystem/data/frames"

CROPPED_DIR = "detected_faces"
BOXED_DIR = "frames_with_face_boxes"

ROTATION = cv2.ROTATE_90_CLOCKWISE
UPSCALE_FACTOR = 1.5

MIN_FACE_SIZE = 25
MIN_DET_SCORE = 0.25


os.makedirs(CROPPED_DIR, exist_ok=True)
os.makedirs(BOXED_DIR, exist_ok=True)

print("=" * 80)
print("[INIT] Loading InsightFace detector (buffalo_l)")
face_app = FaceAnalysis(name="buffalo_l")
face_app.prepare(ctx_id=-1, det_size=(640, 640))
print("[INIT] Detector READY")
print("=" * 80)

face_id = 0
frame_id = 0

for fname in sorted(os.listdir(FRAMES_DIR)):
    frame_id += 1
    print(f"\n FRAME {frame_id}: {fname}")

    path = os.path.join(FRAMES_DIR, fname)
    image = cv2.imread(path)

    if image is None:
        print("  ❌ Frame unreadable → skipped")
        continue

    print(f"  ✔ Frame loaded | Shape: {image.shape}")

    #  ROTATION
    image = cv2.rotate(image, ROTATION)
    print("  ✔ Rotation applied")

    # ROI CROP
    h, w = image.shape[:2]
    image = image[int(0.2*h):int(0.85*h), int(0.2*w):int(0.85*w)]
    print(f"  ✔ ROI crop applied | New shape: {image.shape}")

    # UPSCALE
    image = cv2.resize(
        image, None,
        fx=UPSCALE_FACTOR,
        fy=UPSCALE_FACTOR,
        interpolation=cv2.INTER_CUBIC
    )
    print(f"  ✔ Upscaled by factor {UPSCALE_FACTOR}")

    # LIGHT NORMALIZATION
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(ycrcb)
    y = cv2.equalizeHist(y)
    image = cv2.merge([y, cr, cb])
    image = cv2.cvtColor(image, cv2.COLOR_YCrCb2BGR)
    print("  ✔ Lighting normalized")

    #  FACE DETECTION
    faces = face_app.get(image)

    if len(faces) == 0:
        print("  ❌ NO faces detected by model")
        continue

    print(f"  🔍 Faces detected by model: {len(faces)}")

    valid_faces = 0

    for idx, face in enumerate(faces, start=1):
        print(f"\n    👤 Face {idx}")

        print(f"      • Confidence score: {face.det_score:.3f}")

        if face.det_score < MIN_DET_SCORE:
            print("      ❌ Rejected → LOW CONFIDENCE")
            continue

        x1, y1, x2, y2 = map(int, face.bbox)
        w_box, h_box = x2 - x1, y2 - y1
        print(f"      • Bounding box: {w_box} x {h_box}")

        if w_box < MIN_FACE_SIZE or h_box < MIN_FACE_SIZE:
            print("      ❌ Rejected → FACE TOO SMALL")
            continue

        face_crop = image[y1:y2, x1:x2]

        if face_crop.size == 0:
            print("      ❌ Rejected → INVALID CROP")
            continue

        #  ACCEPT FACE
        face_id += 1
        valid_faces += 1
        face_name = f"FACE_{face_id:06d}.jpg"

        print("       ACCEPTED FACE")
        print(f"       Saved as: {face_name}")

        cv2.imwrite(os.path.join(CROPPED_DIR, face_name), face_crop)

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            image, face_name, (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
        )

    if valid_faces > 0:
        cv2.imwrite(os.path.join(BOXED_DIR, fname), image)
        print(f"\n   FRAME RESULT → {valid_faces} FACE(S) SAVED")
    else:
        print("\n  ⚠ FRAME RESULT → Faces detected BUT all rejected")

print("\n" + "=" * 80)
print("[DONE] Face detection finished")
print(f"[DONE] Total frames processed: {frame_id}")
print(f"[DONE] Total faces saved: {face_id}")
print("=" * 80)
