#!/usr/bin/python

from time import sleep
import pyaudio
import rospy
from std_msgs.msg import String

class AudioMessage(object):
    """Class to publish audio to topic"""

    def __init__(self):

        # initializing publisher with buffer size of 10 messages
        self.pub_ = rospy.Publisher("/sphinx_audio", String, queue_size=10)

        # initialize node
        rospy.init_node("audio_control")
        # call custom function on node shutdown
        rospy.on_shutdown(self.shutdown)

        # all set. publish to topic
        self.transfer_audio_msg()

    #we can add in the boolean from navisystem into this function    
    def transfer_audio_msg(self):
        """Function to publish input audio to topic"""

        rospy.loginfo("audio input node will start after delay of 2 seconds")
        sleep(2)

        stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

        stream.start_stream()

        while not rospy.is_shutdown():
            buf = stream.read(1024)
            if buf:
                self.pub_.publish(buf)

    @staticmethod
    def shutdown():
        """This function is executed on node shutdown."""
        # command executed after Ctrl+C is pressed

        rospy.loginfo("Stop ASRControl")
        rospy.sleep(1)

if __name__ == "__main__":
    AudioMessage()
