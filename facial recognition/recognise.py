import face_recognition
import cv2
import numpy as np
import os

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/5 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Create arrays of known face encodings and their names
known_faces_dir = r"/home/michaellimyuguang/face_recognizer/known_faces"
known_face_encodings = [] #face encodings of the detected faces in the image
known_face_names = [] #the folder name which is used to store the .jpg images

for folder_name in os.listdir(known_faces_dir):
    for file_name in os.listdir(known_faces_dir + r"//" + folder_name):
        image = face_recognition.load_image_file(known_faces_dir + r"//" + folder_name + r"//" + file_name)
        known_face_encoding = face_recognition.face_encodings(image) #face_encodings will detect all the faces in the image. 1 face is encoded in a 128 length array
        if len(known_face_encoding) > 0:
            known_face_encodings.append(known_face_encoding[0]) #we only take the first face detected if the image contain multiply faces
            known_face_names.append(folder_name)


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/5 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.2, fy=0.2)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame) #Returns an array of bounding boxes of human faces in a frame
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations) #Given an image, return the 128-dimension face encoding for each face in the frame.

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding) #matches is a list. length of matches is the same as known_face_encodings. it will be true when similar face encoding from known_face_encodings and face_encodings are found.
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances) #find the smallest distance to the new face
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)
            print(face_names)
    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 5
        right *= 5
        bottom *= 5
        left *= 5
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    # Display the resulting image
    cv2.imshow('Video', frame)
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
