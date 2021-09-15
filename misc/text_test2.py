import cv2
import rospy
import pytesseract
from pytesseract import Output
# from locobot_control.msg import Detection # Import custom message
from sensor_msgs import Image
from cv_bridge import CvBridge, CvBridgeError


# def image_callback(message):
#     bridge = CvBridge() 
#     try:
#         cv_image = bridge.imgmsg_to_cv2(message.image, "bgr8")
        
#         d = pytesseract.image_to_data(cv_image, output_type=Output.DICT)
#         n_boxes = len(d['level'])
#         # print(d.keys())
#         for i in range(n_boxes):
#             # print(d['word_num'][i],d['text'][i],d['conf'][i])
#             if d['word_num'][i] != 0 and d['text'][i] != '':
#                 # print(d['text'][i] == '')
#                 # rospy.loginfo("word_num: %s" % d['word_num'][i])
#                 rospy.loginfo("detected %s, confidence = %d" % (d['text'][i], d['conf'][i]))
#                 (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
#                 cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

#         cv2.imshow("Image Window", cv_image)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             cv2.destroyAllWindows()

#     except CvBridgeError, e:
#         cv2.destroyAllWindows()
#         print(e)

def image_callback(image):
    bridge = CvBridge() 
    try:
        cv_image = bridge.imgmsg_to_cv2(image, "bgr8")
        
        d = pytesseract.image_to_data(cv_image, output_type=Output.DICT)
        n_boxes = len(d['level'])
        # print(d.keys())
        for i in range(n_boxes):
            # print(d['word_num'][i],d['text'][i],d['conf'][i])
            if d['word_num'][i] != 0 and d['text'][i] != '':
                # print(d['text'][i] == '')
                # rospy.loginfo("word_num: %s" % d['word_num'][i])
                rospy.loginfo("detected %s, confidence = %d" % (d['text'][i], d['conf'][i]))
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Image Window", cv_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    except CvBridgeError, e:
        cv2.destroyAllWindows()
        print(e)        


def main():
    rospy.init_node('Text_Recognition_NODE')
    rospy.Subscriber("/camera/color/image_raw", Image, image_callback, queue_size=1)    # sensor_msgs/Image
    # rospy.Subscriber("/camera/color/image_raw/compressed", Image, image_callback, queue_size=1)    # sensor_msgs/CompressedImage
    # rospy.Subscriber("image_topic", Detection, image_callback, queue_size=2)
    rospy.spin()    

if __name__ == "__main__":    
    main()
    