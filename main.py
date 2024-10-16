import cv2
import numpy as np
import csv
from datetime import datetime
import face_recognition

print('Attendance using Face Recognition \n')
print("Face Recognition version:", face_recognition.__version__)

video_capture = cv2.VideoCapture(1)
# Load known faces
img1 = face_recognition.load_image_file("Faces/Hemant.jpg")
img1_encoding = face_recognition.face_encodings(img1)[0]
img2 = face_recognition.load_image_file("Faces/Ved.jpg")
img2_encoding = face_recognition.face_encodings(img2)[0]
img4 = face_recognition.load_image_file("Faces/Subodh.jpg")
img4_encoding = face_recognition.face_encodings(img4)[0]
# img3 = face_recognition.load_image_file("Faces/Yash.jpg")
# img3_encoding = face_recognition.face_encodings(img1)[0]

known_face_encodings = [img1_encoding, img2_encoding, img4_encoding]
known_face_names = ['Hemant', 'Ved', 'Subodh']

# List of expected students
students = known_face_names.copy()
face_locations = []
face_encodings = []

# Get the current date and time
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
f = open(f"{current_date}.csv", "w+", newline="")
lnwriter = csv.writer(f)

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Recognize faces
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distance)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            if name in students:
                students.remove(name)
                cur_time = now.strftime('%H.%M.%S')
                lnwriter.writerow([name, cur_time])

            # Display name for recognized faces
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (10, 100)
            fontScale = 1.5
            fontColor = (255, 0, 0)
            thickness = 3
            lineType = 2
            cv2.putText(frame, name + " Identified", bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType)

        else:
            # Display "Entry Denied" for unknown faces
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (10, 100)
            fontScale = 1.5
            fontColor = (0, 0, 255)  # Red color for denial
            thickness = 3
            lineType = 2
            cv2.putText(frame, "Unidentified Faced", bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType)

    cv2.imshow("Face Identifier", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
