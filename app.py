from flask import Flask, render_template, Response, jsonify
import cv2
import face_recognition
import numpy as np
import os

app = Flask(__name__)

# Path to the folder containing known face images
KNOWN_FACES_DIR = "Faces/"
known_face_encodings = []
known_face_names = []


# Load known faces from the Faces folder
def load_known_faces():
    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # Load the image and extract the name
            img_path = os.path.join(KNOWN_FACES_DIR, filename)
            img = face_recognition.load_image_file(img_path)
            img_encoding = face_recognition.face_encodings(img)[0]

            # Store the encoding and the corresponding name (use filename without extension as name)
            known_face_encodings.append(img_encoding)
            known_face_names.append(os.path.splitext(filename)[0])


# Call the function to load faces
load_known_faces()


# Function to generate camera frames
def generate_frames():
    video_capture = cv2.VideoCapture(1)  # Use webcam (0 for built-in camera, 1 for external)
    while True:
        success, frame = video_capture.read()
        if not success:
            break

        # Process frame for face recognition
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distance)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

                # Display name for recognized faces
                cv2.putText(frame, f"{name} Identified", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)
            else:
                # Display "Unidentified" for unknown faces
                cv2.putText(frame, "Unidentified Face", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

        # Encode the frame to JPEG and yield it
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    # Render the HTML page
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    # Return the video feed
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
