import os
import cv2
import numpy as np
import pickle
from insightface.app import FaceAnalysis
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- CONFIG ----------------
FACE_FOLDER = "frames_with_face_boxes"
SIM_THRESHOLD = 0.6
EMB_FILE = "customer_embeddings.pkl"
RESULT_FILE = "recognition_results.csv"

# ----------------------------------------

# Load face model
app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=0, det_size=(640, 640))

customer_db = {}   # customer_id -> mean_embedding
results = []

customer_counter = 1

# Process each face image
for img_name in sorted(os.listdir(FACE_FOLDER)):
    img_path = os.path.join(FACE_FOLDER, img_name)
    img = cv2.imread(img_path)

    if img is None:
        continue

    faces = app.get(img)
    if len(faces) == 0:
        continue

    emb = faces[0].embedding
    matched = False

    for cust_id, cust_emb in customer_db.items():
        sim = cosine_similarity(
            emb.reshape(1, -1),
            cust_emb.reshape(1, -1)
        )[0][0]

        if sim >= SIM_THRESHOLD:
            # Existing customer
            customer_db[cust_id] = (cust_emb + emb) / 2
            results.append([img_name, cust_id, sim])
            matched = True
            break

    if not matched:
        # New customer
        cust_id = f"CUST_{customer_counter:04d}"
        customer_db[cust_id] = emb
        results.append([img_name, cust_id, 1.0])
        customer_counter += 1

# Save embeddings
with open(EMB_FILE, "wb") as f:
    pickle.dump(customer_db, f)

# Save results
with open(RESULT_FILE, "w") as f:
    f.write("image_name,customer_id,similarity\n")
    for r in results:
        f.write(f"{r[0]},{r[1]},{r[2]:.2f}\n")

print(" Recognition completed")
print(f" Total unique customers: {len(customer_db)}")
print(f" Embeddings saved to: {EMB_FILE}")
print(f" Results saved to: {RESULT_FILE}")
