import mysql.connector as mysql
import numpy as np
import cv2
from deepface import DeepFace

def connect_db():
    return mysql.connect(
        host="localhost",
        user="root",
        password="",
        database="smartFace"
    )

def blob_to_image(blob):
    try:
        nparr = np.frombuffer(blob, np.uint8)
        return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    except Exception as e:
        print("Erreur décodage image:", e)
        return None

def is_same_face(img1, img2):
    try:
        result = DeepFace.verify(img1, img2, enforce_detection=False)
        return result["verified"]
    except Exception as e:
        print("Erreur comparaison DeepFace:", e)
        return False

def update_or_insert_attendance(db, emp_id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM attendance WHERE employee_id = %s AND DATE(date) = CURDATE()", (emp_id,))
    if cursor.fetchone():
        print(f"📌 Employé {emp_id} déjà pointé aujourd’hui.")
    else:
        cursor.execute("INSERT INTO attendance (employee_id) VALUES (%s)", (emp_id,))
        db.commit()
        print(f"✅ Présence enregistrée pour employé {emp_id}.")

def main():
    print("✅ Démarrage de l'application...")

    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT employee_id, image FROM employees")
        data = cursor.fetchall()
        print(f"📦 {len(data)} employés chargés depuis la base.")
    except Exception as e:
        print("❌ Erreur connexion base ou chargement employés:", e)
        return

    known_faces = []
    known_ids = []

    for emp_id, blob in data:
        img = blob_to_image(blob)
        if img is not None:
            known_faces.append(img)
            known_ids.append(emp_id)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Erreur: caméra non détectée.")
        return

    print("🎥 Caméra active. Appuyez sur Q pour quitter.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Échec lecture caméra.")
            break

        detected = False

        for i, known_img in enumerate(known_faces):
            if is_same_face(frame, known_img):
                emp_nom = known_ids[i]
                update_or_insert_attendance(db, emp_nom)
                cv2.putText(frame, f"Employe : {emp_nom} ", (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)
                detected = True
                break

        if not detected:
            cv2.putText(frame, "Visage non reconnu", (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2)

        cv2.imshow("Reconnaissance Faciale", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    db.close()
    print("🛑 Application arrêtée.")

if __name__ == "__main__":
    main()
