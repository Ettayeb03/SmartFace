import cv2
import numpy as np
from deepface import DeepFace
import datetime

def find_encodings(images):
    encode_list = []
    for img in images:
        if img.shape[2] == 4:
            img = img[:, :, :3]
        try:
            emb = DeepFace.represent(img_path=img, model_name='Facenet', enforce_detection=False)
            encode_list.append(emb[0]['embedding'])
        except:
            encode_list.append(None)
    return encode_list

def recognize_faces_in_frame(known_encodings, frame):
    try:
        results = DeepFace.extract_faces(img_path=frame, detector_backend='opencv', enforce_detection=False)
        if not results:
            return False, None, None
        face = results[0]
        x, y, w, h = face['facial_area'].values()
        face_loc = (y, x + w, y + h, x)
        embedding = DeepFace.represent(img_path=frame, model_name='Facenet', enforce_detection=False)[0]['embedding']

        min_dist = float('inf')
        idx = None
        for i, known in enumerate(known_encodings):
            if known is None:
                continue
            dist = np.linalg.norm(np.array(embedding) - np.array(known))
            if dist < min_dist:
                min_dist = dist
                idx = i
        return (min_dist < 0.6), idx, face_loc
    except Exception as e:
        print("Erreur DeepFace:", e)
        return False, None, None

def update_attendance(connection, employee_id):
    cursor = connection.cursor()
    now = datetime.datetime.now()
    cursor.execute("""
        SELECT status, MAX(date) as date FROM attendance 
        WHERE employee_id = %s GROUP BY status
    """, (employee_id,))
    records = cursor.fetchall()

    status = 'in'
    if records:
        last = max(records, key=lambda r: r[1])
        if last[0] == 'in':
            status = 'out'
    cursor.execute("INSERT INTO attendance (employee_id, status, date) VALUES (%s, %s, %s)", (employee_id, status, now))
    connection.commit()
    cursor.close()
