#!/usr/bin/env python
from pyrobot import Robot
import rospy
from locobot_control.msg import Detection # Import custom message Detection.msg
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import dlib

def main():
    detector = dlib.get_frontal_face_detector()

    rospy.init_node('IMAGE_PUBLISH_NODE')
    # pub = rospy.Publisher('image_topic', Detection, queue_size=10)
    pub = rospy.Publisher('image_topic', Image, queue_size=2)
    cap = cv2.VideoCapture(0)
    bridge = CvBridge()
    rate = rospy.Rate(100) # 10hz


    while not rospy.is_shutdown():
        _, img = cap.read()
        # image_msg = bridge.cv2_to_imgmsg(img, "bgr8")
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # faces = detector(gray)
        # detections = []
        # message = Detection()   # message = Detection.msg

        # if len(faces) > 0:
            # print(len(faces))
            # for face in faces:
            #     x = face.left()
            #     y = face.top()
            #     w = face.right()
            #     h = face.bottom()
            #     pt1 = (x, y)
            #     pt2 = (w, h)
            #     detections.append((pt1[0], pt1[1], pt2[0], pt2[1]))

            # print(pt1)
            # print(len(detections))
            # print(detections[1])
            # print(detections[:][1])
            # message.x = detections[:][0]
            # message.y = detections[:][1]
            # message.w = detections[:][2]
            # message.h = detections[:][3]


        # message.x = [1]
        # message.y = [2]
        message = Image()
        message = bridge.cv2_to_imgmsg(img, "bgr8")
        pub.publish(message)
        rate.sleep()




if __name__ == "__main__":
    main()
