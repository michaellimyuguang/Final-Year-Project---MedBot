import cv2
import rospy
from locobot_control.msg import Detection # Import custom message Detection.msg
from cv_bridge import CvBridge, CvBridgeError

def main():
    rospy.init_node('IMAGE_PUBLISH_NODE')
    pub = rospy.Publisher('image_topic', Detection, queue_size=10)   
    cap = cv2.VideoCapture(0)
    bridge = CvBridge() 
    rate = rospy.Rate(100) # 10hz


    while not rospy.is_shutdown():
        _, img = cap.read()
        image_msg = bridge.cv2_to_imgmsg(img, "bgr8")
        message = Detection()   # message = Detection.msg
        message.image = bridge.cv2_to_imgmsg(img, "bgr8")
        pub.publish(message)
        rate.sleep()

    cap.release()



if __name__ == "__main__":    
    main()
    