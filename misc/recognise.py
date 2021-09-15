import face_recognition
import cv2
import numpy as np
import os
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

#video_capture = cv2.VideoCapture(0)

# Get a reference to webcam #0 (the default one)

def image_callback(data):
    bridge = CvBridge()
    try:
        frame = bridge.imgmsg_to_cv2(data, "bgr8")
        # Initialize some variables

        #while True:
            # Grab a single frame of video
            #ret, frame = video_capture.read()

            # Resize frame of video to 1/5 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.2, fy=0.2)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame) #Returns an array of bounding boxes of human faces in a frame
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations) #Given an image, return the 128-dimension face encoding for each face in the image.

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/5 size
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
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    except CvBridgeError as e:
        cv2.destroyAllWindows()
        print(e)

def img_callback_test(msg):
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
    cv2.imshow("OpenCV object detection", cv_image)

def main():
    rospy.init_node('Face_Recognition_NODE')
    # rospy.Subscriber("/camera/color/image_raw", Image, image_callback, queue_size=2)    # sensor_msgs/Image
    rospy.Subscriber("/camera/color/image_raw", Image, img_callback_test, queue_size=2)
    rospy.spin()

if __name__ == "__main__":
    # global face_locations = []
    # global face_encodings = []
    # global face_names = []
    #
    # # Create arrays of known face encodings and their names
    # global KNOWN_FACES_DIR = r"/home/locobot/low_cost_ws/src/pyrobot/robots/LoCoBot/locobot_control/known_faces"
    # global known_face_encodings = [] #face encodings of all the detected faces in the image
    # global known_face_names = [] #the folder name which is used to store the .jpg images
    #
    # for name in os.listdir(KNOWN_FACES_DIR):
    #     for filename in os.listdir(KNOWN_FACES_DIR + r"//" + name):
    #         image = face_recognition.load_image_file(KNOWN_FACES_DIR + r"//" + name + r"//" + filename)
    #         known_face_encoding = face_recognition.face_encodings(image) #face_encodings will detect all the faces in the image
    #         if len(known_face_encoding) > 0:
    #             known_face_encodings.append(known_face_encoding[0]) #we only take the first face detected
    #             known_face_names.append(name)
    main()
