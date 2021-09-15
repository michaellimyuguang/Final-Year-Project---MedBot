import face_recognition
import os
import cv2
import numpy as np

KNOWN_FACES_DIR = 'known_faces'
TOLERANCE = 0.6
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = 'cnn'

video = cv2.VideoCapture(0)

print('Loading known faces...')
known_faces = []
known_names = []

for name in os.listdir(KNOWN_FACES_DIR):
    for filename in os.listdir(KNOWN_FACES_DIR + r"//" + name):
        image = face_recognition.load_image_file(KNOWN_FACES_DIR + r"//" + name + r"//" + filename)
        encoding = face_recognition.face_encodings(image)[0]
        if len(encoding > 0):
            known_faces.append(encoding)
            known_names.append(name)


print('Processing unknown faces...')
while True:
    ret, image = video.read()
    # Resize frame of video to 1/5 size for faster face recognition processing
    small_frame = cv2.resize(image, (0, 0), fx=0.2, fy=0.2)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    locations = face_recognition.face_locations(rgb_small_frame, model=MODEL)
    encodings = face_recognition.face_encodings(rgb_small_frame, locations)
    for face_encoding, face_location in zip(encodings, locations):
        results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
        match = None
        if True in results:
            match = known_names[results.index(True)]
            print('Match found: ' + str(match))

            # Each location contains positions in order: top, right, bottom, left
            top_left = (face_location[3] * 5 , face_location[0] * 5) #(left, top)
            bottom_right = (face_location[1] * 5, face_location[2] * 5) #(right, bottom)
            color = [0, 255, 0]
            cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

            top_left = (face_location[3] * 5, face_location[2] * 5 - 35)
            bottom_right = (face_location[1] * 5, face_location[2] * 5)
            cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
            cv2.putText(image, match, (face_location[3] * 5 + 6, face_location[2] * 5 - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)

    cv2.imshow(filename, image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
