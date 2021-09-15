from pyrobot import Robot
import rospy
# from locobot_control.msg import Detection # Import custom message
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

# def image_callback(message):
#     bridge = CvBridge()
#     try:
#         # pt1 = (message.x, message.y)
#         # pt2 = (message.w, message.h)
#         # rospy.loginfo("x = %d" % (message.x))
#         cv_image = bridge.imgmsg_to_cv2(message.image, "bgr8")
#         cv2.imshow(CV_WINDOW_TITLE, cv_image)
#         # cv2.rectangle(cv_image, pt1, pt2, (0, 255, 0), thickness=2)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             cv2.destroyAllWindows()

#     except CvBridgeError, e:
#         cv2.destroyAllWindows()
#         print(e)

def image_callback(data):
    bridge = CvBridge()
    try:
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
        cv2.imshow("OpenCV object detection", cv_image)
        # cv2.rectangle(cv_image, pt1, pt2, (0, 255, 0), thickness=2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    except CvBridgeError, e:
        cv2.destroyAllWindows()
        print(e)

def main():
    rospy.init_node('IMAGE_Receive_NODE')
    rospy.Subscriber("/camera/color/image_raw", Image, image_callback, queue_size=2)
    # rospy.Subscriber("image_topic", Detection, image_callback, queue_size=1)
    rospy.spin()


if __name__ == "__main__":
    main()
